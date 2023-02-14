import os
import platform
import subprocess
from pathlib import Path

import requests
from tqdm import tqdm

from rift.runtime.config import Config


class RiftLibSetup:
    version = 3
    urls = {
        "windows": "https://github.com/AminRezaei0x443/ton/releases/download/v0.1.5/rift-lib-win64.dll",
        "darwin": "https://github.com/AminRezaei0x443/ton/releases/download/v0.1.5/rift-lib-macOS.dylib",
        "darwin-slc": "https://github.com/AminRezaei0x443/ton/releases/download/v0.1.5/rift-lib-macOS-silicon.dylib",
        "linux-u18": "https://github.com/AminRezaei0x443/ton/releases/download/v0.1.5/rift-lib-ubuntu-18.04.so",
        "linux-u20": "https://github.com/AminRezaei0x443/ton/releases/download/v0.1.5/rift-lib-ubuntu-20.04.so",
        "linux-u22": "https://github.com/AminRezaei0x443/ton/releases/download/v0.1.5/rift-lib-ubuntu-22.04.so",
    }

    @classmethod
    def acquire_lib(cls, ensure=False) -> str:
        if ensure:
            cls.setup_riftlib()
        return os.path.join(Config.dirs.user_data_dir, "_riftlib.pyd")

    @classmethod
    def is_setup(cls) -> bool:
        version_file = os.path.join(Config.dirs.user_data_dir, "_rl_version")
        if not os.path.exists(version_file):
            return False
        with open(version_file, "r") as vf:
            version = vf.read()
        version = int(version)
        if version < cls.version:
            return False
        return os.path.exists(cls.acquire_lib())

    @classmethod
    def _ubuntu_version(cls) -> int:
        try:
            if os.path.exists("/etc/lsb-release"):
                with open("/etc/lsb-release") as f:
                    c = f.read().strip()
                lines = c.split("\n")
                info = dict(map(lambda x: x.split("="), lines))
                if info["DISTRIB_ID"].lower() == "ubuntu":
                    return int(info["DISTRIB_RELEASE"].split(".")[0])
            return -1
        except Exception:
            return -1

    @classmethod
    def determine_lib(cls) -> str:
        s = platform.uname().system.lower()
        if s == "windows":
            return cls.urls[s]
        if s == "darwin":
            proc = platform.processor()
            if proc == "i386":
                return cls.urls[s]
            elif proc == "arm":
                return cls.urls[f"{s}-slc"]
            else:
                raise RuntimeError(f"Unknown processor: {proc}")
        uv = cls._ubuntu_version()
        if uv == -1:
            raise RuntimeError("Unsupported os")
        return cls.urls[f"linux-u{uv}"]

    @classmethod
    def _call_get(cls, command):
        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if p.returncode == 0:
            return True, out.decode("utf-8")
        return False, err.decode("utf-8")

    @classmethod
    def get_shared_libs(cls):
        ok, res = cls._call_get(["ldconfig", "-p"])
        if not ok:
            raise RuntimeError("Error fetching shared libraries!")
        res = filter(lambda x: "=>" in x, res.split("\n"))
        res = map(
            lambda x: list(map(lambda f: f.strip(), x.split("=>"))),
            res,
        )
        libs = dict(res)
        return libs

    @classmethod
    def get_glibc_version(cls):
        ok, res = cls._call_get(["ldconfig", "--version"])
        if not ok:
            raise RuntimeError("Error fetching glibc version!")
        return res.split("\n")[0].split(" ")[-1].strip()

    @classmethod
    def get_env_info(cls):
        return {
            "libs": cls.get_shared_libs(),
            "glibc": cls.get_glibc_version(),
        }

    @classmethod
    def _download(cls, addr: str, to: str, buffer=1024):
        response = requests.get(addr, stream=True)
        file_size = int(response.headers.get("Content-Length"))
        pbar = tqdm(total=file_size, unit="B", unit_scale=True)
        with open(to, "wb") as f:
            for chunk in response.iter_content(chunk_size=buffer):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    pbar.update(buffer)
        pbar.close()

    @classmethod
    def setup_riftlib(cls):
        lib_path = cls.acquire_lib()
        if cls.is_setup():
            return
        url = cls.determine_lib()
        os.makedirs(
            Path(lib_path).parent.absolute(), mode=0o777, exist_ok=True,
        )
        version_file = os.path.join(Config.dirs.user_data_dir, "_rl_version")
        with open(version_file, "w") as vf:
            vf.write(str(cls.version))
        cls._download(url, lib_path, buffer=4096)
