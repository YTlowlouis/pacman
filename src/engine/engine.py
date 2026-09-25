import json
from pathlib import Path
import pygame

from src.models import Config, PointsConfig, LevelConfig, PacManConfig
from src.engine.scenes.scene_menu import MenuScene
from src.engine.scenes.scene_baseclass import Scene
from src.engine.scenes.scene_scoreboard import ScoreBoard
from src.engine.scenes.scene_gameover import GameOverScene
from src.engine.scenes.scene_running import RunningScene
from src.engine.scenes.scene_pause import PauseScene
from src.engine.wave_manager import WaveManager


class ConfigFileError(Exception):
    pass


class Engine:
    DEFAULT_LIVES = 3
    DEFAULT_POINTS = {"ghost": 200, "super_pacgum": 50, "pacgum": 10}
    DEFAULT_LEVEL = {
        "height": 15,
        "width": 15,
        "max_time": 120,
    }
    DEFAULT_PACMAN = {
        "dir": "right",
        "next_dir": "right",
        "sprite": "src/assets/pacman.png",
    }
    MIN_MAZE_SIZE = 3
    MAX_MAZE_SIZE = 60

    def __init__(self, config_file: str):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 900))
        self.clock = pygame.time.Clock()
        self.running = True

        self.wave_manager = WaveManager()
        self.config: Config
        self.load_conf(config_file)

        self.scene: Scene = MenuScene(self)
        self.scenes = {
            "Menu": self.scene,
            "Score": ScoreBoard(self),
            "GameOver": GameOverScene(self),
            "Running": RunningScene(self),
            "Pause": PauseScene(self)
        }
        self._next_scene: Scene | None = None

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

            if self._next_scene is not None:
                self.scene = self._next_scene
                self._next_scene = None

        pygame.quit()

    def change_scene(self, scene: Scene) -> None:
        self._next_scene = scene

    @staticmethod
    def _warn(message: str) -> None:
        print(f"config: {message}")

    def _get_int(
        self,
        source: dict,
        key: str,
        default: int,
        minimum: int | None = None,
        maximum: int | None = None,
        where: str = "",
        quiet: bool = False,
    ) -> int:
        value = source.get(key)
        if value is None:
            if not quiet:
                self._warn(f"{where}missing '{key}', using {default}")
            return default
        if isinstance(value, bool) or not isinstance(value, int):
            self._warn(
                f"{where}'{key}' is not an integer ({value!r}), "
                f"using {default}"
            )
            return default
        if minimum is not None and value < minimum:
            self._warn(f"{where}'{key}' {value} clamped to {minimum}")
            return minimum
        if maximum is not None and value > maximum:
            self._warn(f"{where}'{key}' {value} clamped to {maximum}")
            return maximum
        return value

    def _read_options(self, config_file: str) -> dict:
        try:
            with open(config_file, "r") as file:
                text = "".join(
                    line for line in file if not line.lstrip().startswith("#")
                )
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
            options = json.loads(text)
        except json.JSONDecodeError as e:
            raise ConfigFileError(f"Invalid JSON in {config_file}: {e}")

        if not isinstance(options, dict):
            raise ConfigFileError(
                f"{config_file}: top level must be a JSON object"
            )
        return options

    def _build_points(self, options: dict) -> PointsConfig:
        raw = options.get("points_per")
        if not isinstance(raw, dict):
            self._warn("missing or invalid 'points_per', using defaults")
            raw = {}
        return PointsConfig(
            ghost=self._get_int(
                raw,
                "ghost",
                self.DEFAULT_POINTS["ghost"],
                minimum=0,
                where="points_per: ",
            ),
            super_pacgum=self._get_int(
                raw,
                "super_pacgum",
                self.DEFAULT_POINTS["super_pacgum"],
                minimum=0,
                where="points_per: ",
            ),
            pacgum=self._get_int(
                raw,
                "pacgum",
                self.DEFAULT_POINTS["pacgum"],
                minimum=0,
                where="points_per: ",
            ),
        )

    def _build_levels(self, options: dict) -> list[LevelConfig]:
        raw_levels = options.get("levels")
        if not isinstance(raw_levels, list) or not raw_levels:
            self._warn("missing or empty 'levels', using one default level")
            raw_levels = [dict(self.DEFAULT_LEVEL)]

        levels = []
        for index, raw in enumerate(raw_levels):
            where = f"level #{index + 1}: "
            if not isinstance(raw, dict):
                self._warn(f"{where}not an object, using defaults")
                raw = dict(self.DEFAULT_LEVEL)
            levels.append(
                LevelConfig(
                    id=self._get_int(
                        raw,
                        "id",
                        index + 1,
                        minimum=0,
                        where=where,
                        quiet=True,
                    ),
                    height=self._get_int(
                        raw,
                        "height",
                        self.DEFAULT_LEVEL["height"],
                        minimum=self.MIN_MAZE_SIZE,
                        maximum=self.MAX_MAZE_SIZE,
                        where=where,
                    ),
                    width=self._get_int(
                        raw,
                        "width",
                        self.DEFAULT_LEVEL["width"],
                        minimum=self.MIN_MAZE_SIZE,
                        maximum=self.MAX_MAZE_SIZE,
                        where=where,
                    ),
                    max_time=self._get_int(
                        raw,
                        "max_time",
                        self.DEFAULT_LEVEL["max_time"],
                        minimum=1,
                        where=where,
                    ),
                    seed=self._get_int(
                        raw,
                        "seed",
                        0,
                        minimum=0,
                        where=where,
                        quiet=True,
                    ),
                )
            )
        return levels

    def _build_pacman_conf(self, options: dict) -> PacManConfig:
        raw = options.get("pacman")
        if not isinstance(raw, dict):
            self._warn("missing or invalid 'pacman', using defaults")
            raw = {}

        sprite = raw.get("sprite")
        if not isinstance(sprite, str):
            sprite = self.DEFAULT_PACMAN["sprite"]
            self._warn(f"pacman: invalid 'sprite', using {sprite}")

        return PacManConfig(
            dir=self.DEFAULT_PACMAN["dir"],
            next_dir=self.DEFAULT_PACMAN["next_dir"],
            sprite=Path(sprite),
        )

    def load_conf(self, config_file: str) -> None:
        options = self._read_options(config_file)
        self.config = Config(
            levels=self._build_levels(options),
            points=self._build_points(options),
            lives=self._get_int(
                options, "lives", self.DEFAULT_LIVES, minimum=1
            ),
            pacman=self._build_pacman_conf(options),
        )
