import json
from enum import Enum

from pydantic import ValidationError
import pygame

from src.models import Config, PointsConfig, LevelConfig
from src.engine.scenes.scene_menu import MenuScene
from src.engine.scenes.scene_baseclass import Scene


class ConfigFileError(Exception):
    pass


class State(Enum):
    MENU = "menu"
    PLAYING = "playing"


class Engine:
    def __init__(self, config_file: str):
        self.config: Config
        self.load_conf(config_file)
        pygame.init()
        self.screen = pygame.display.set_mode((800, 900))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene: Scene = MenuScene()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene.handle_event(event)

            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    def change_scene(self, scene: Scene) -> None:
        self.scene = scene

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
