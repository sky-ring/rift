from setuptools import Extension
from setuptools.command.build_ext import build_ext
import os
import platform
import requests
from tqdm import tqdm


class BuildFailed(Exception):
    pass


class GetRiftLib(build_ext):
    """Customized build command to get rift lib"""

    urls = {
        "windows": "https://github.com/AminRezaei0x443/ton/releases/download/v0.1.0/rift-lib-win64.dll",
        "darwin": "https://github.com/AminRezaei0x443/ton/releases/download/v0.1.0/rift-lib-macOS.dylib",
        "linux": "https://github.com/AminRezaei0x443/ton/releases/download/v0.1.0/rift-lib-ubuntu-22.04.so",
    }

    @staticmethod
    def download(addr: str, to: str, buffer=1024):
        response = requests.get(addr, stream=True)
        file_size = int(response.headers.get('Content-Length'))
        pbar = tqdm(total=file_size, unit='B', unit_scale=True)

        with open(to, 'wb') as f:
            for chunk in response.iter_content(chunk_size=buffer):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    pbar.update(buffer)

        pbar.close()

    def build_extension(self, ext):
        # Let's detect platform
        os_ = platform.uname().system.lower()
        url = self.urls[os_]
        ext_path = os.path.join(os.getcwd(), self.get_ext_fullpath(ext.name))
        self.download(url, ext_path)


ext_modules = [
    Extension('_riftlib', []),
]


def build(setup_kwargs):
    setup_kwargs.update(
        {"ext_modules": ext_modules, "cmdclass": {"build_ext": GetRiftLib}},
    )


def build_kwargs():
    return {"ext_modules": ext_modules, "cmdclass": {"build_ext": GetRiftLib}}
