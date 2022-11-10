from os import getcwd, path

from tomlkit import parse


class ContractConfig:
    name: str | None
    contract: str
    tests: list[str]
    deploys: list[str]

    @classmethod
    def load(cls, data: dict) -> "ContractConfig":
        config = ContractConfig()
        config.name = data.get("name", None)
        config.contract = data["contract"]
        config.tests = data.get("tests", [])
        config.deploys = data.get("deploys", [])
        return config


class ProjectConfig:
    name: str
    contracts: dict[str, ContractConfig]

    @classmethod
    def load(cls, path_: str) -> "ProjectConfig":
        with open(path_) as f:
            content = f.read()
        doc = parse(content)
        config = ProjectConfig()
        config.name = doc["name"]
        contracts = doc["contracts"]
        config.contracts = {}
        for c in contracts:
            config.contracts[c] = ContractConfig.load(contracts[c])
        return config

    @classmethod
    def working(cls) -> "ProjectConfig | None":
        """Loads config from the working directory

        Returns None if not a project
        """
        cwd = getcwd()
        config_file = path.join(cwd, "project.toml")
        if not path.exists(config_file):
            return None
        return cls.load(config_file)
