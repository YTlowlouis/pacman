import json


class ConfigFileError(Exception):
    pass


class Engine:
    def __init__(self, config_file: str):
        self.load_conf(config_file)

    def load_conf(self, config_file: str) -> None:
        try:
            with open(config_file, "r") as file:
                text = "".join(
                    line for line in file if not line.startswith("#")
                )
            options = json.loads(text)
        except Exception as e:
            raise ConfigFileError(f"{e}")
