from os import EX_CANTCREAT

from pydantic import ValidationError
import json

from src.models import Config, PointsConfig, LevelConfig


class ConfigFileError(Exception):
    pass


class Engine:
    def __init__(self, config_file: str):
        self.config: Config
        self.load_conf(config_file)

    def load_conf(self, config_file: str) -> None:
        try:
            with open(config_file, "r") as file:
                text = "".join(
                    line for line in file if not line.startswith("#")
                )
            options = json.loads(text)
        except FileNotFoundError:
            raise ConfigFileError(f"File: {config_file} does not exist")
        except PermissionError:
            raise ConfigFileError(
                f"Invalid permissions for file: {config_file}"
            )
        except OSError as e:
            raise ConfigFileError(
                f"Error open or reading file: {config_file}, {e}"
            )

        try:
            points_conf = PointsConfig(
                ghost=options["points_per"]["ghost"],
                super_pacgum=options["points_per"]["super_pacgum"],
                pacgum=options["points_per"]["pacgum"],
            )
        except KeyError as e:
            raise ConfigFileError(
                f"missing option in config file for points, {e}"
            )
        except ValidationError as e:
            raise ConfigFileError(
                f"Invalid option in config file for points: {e.errors()}"
            )

        levels = []
        try:
            for level in options["levels"]:
                levels.append(
                    LevelConfig(
                        id=level["id"],
                        height=level["height"],
                        width=level["width"],
                        max_time=level["max_time"],
                    )
                )
        except KeyError as e:
            raise ConfigFileError(f"Missing option in level config, : {e}")
        except ValidationError as e:
            raise ConfigFileError(
                f"Invalid option in config file for levels: {e.errors()}"
            )
        try:
            lives = options["lives"]
        except KeyError:
            raise ConfigFileError("Missing lives parameter")
        except ValidationError as e:
            raise ConfigFileError(f"Invalid lives parameter: {e}")

        self.config = Config(levels=levels, points=points_conf, lives=lives)
        print(self.config)
