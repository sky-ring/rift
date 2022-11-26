import re
from os import getcwd, path

from tomlkit import parse


class ContractConfig:
    name: str | None
    contract: str
    tests: list[str]
    deploy: str | None

    def get_file_name(self) -> str:
        name = self.name
        if name is None:
            name = self.contract
            # CamelCase -> snake_case
            name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        return name

    @classmethod
    def load(cls, data: dict) -> "ContractConfig":
        config = ContractConfig()
        config.name = data.get("name", None)
        config.contract = data["contract"]
        config.tests = data.get("tests", [])
        config.deploy = data.get("deploy", None)
        return config


class ProjectConfig:
    name: str
    contracts: dict[str, ContractConfig]

    def get_contract(self, name: str) -> ContractConfig:
        for contract_cfg in self.contracts.values():
            if contract_cfg.contract == name:
                return contract_cfg
        return ContractConfig.load({"contract": name})

    def get_contract_file_name(self, contract: type | str):
        if isinstance(contract, type):
            contract = contract.__name__
        cfg = self.get_contract(contract)
        return cfg.get_file_name()

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
