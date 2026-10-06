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
from src.engine.scenes.scene_instructions import InstructionsScene
from src.engine.wave_manager import WaveManager


class ConfigFileError(Exception):
    """Raised when the config file is missing, unreadable or not JSON."""

    pass


class Engine:
    """Owns the window, the game loop, the scenes and the config."""

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
    }
    FIRST_LEVEL_SEED = 42
    MIN_MAZE_SIZE = 3
    MAX_MAZE_SIZE = 60

    def __init__(self, config_file: Path):
        """Open the window, load the config and create every scene.

        Args:
            config_file: Path of the JSON config file.

        Raises:
            ConfigFileError: If the config file cannot be read.
            MazeGenerationError: If the first maze cannot be generated.
        """
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
            "Pause": PauseScene(self),
            "Instructions": InstructionsScene(self),
        }
        self._next_scene: Scene | None = None

    def run(self) -> None:
        """Run the game loop until the player quits.

        Each frame dispatches the events, updates and draws the current
        scene, then applies any pending scene change. The window is
        always closed, even if an error stops the loop.
        """
        try:
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
        finally:
            pygame.quit()

    def change_scene(self, scene: Scene) -> None:
        """Switch to another scene at the end of the current frame.

        Args:
            scene: Scene to show next.
        """
        self._next_scene = scene

    @staticmethod
    def _warn(message: str) -> None:
        """Print a config warning.

        Args:
            message: Text to print.
        """
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
        """Read an integer option, with a default and optional bounds.

        Args:
            source: Dict to read from.
            key: Option name.
            default: Value used when the option is missing or not an
                integer.
            minimum: Lowest allowed value, if any.
            maximum: Highest allowed value, if any.
            where: Prefix telling where the option is, for warnings.
            quiet: If True, do not warn when the option is missing.

        Returns:
            The option value, or the default or bound that replaces it.
        """
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
        return int(value)

    def _read_options(self, config_file: Path) -> dict:
        """Read the config file, skipping lines that start with ``#``.

        Args:
            config_file: Path of the config file, as given on the
                command line.

        Returns:
            The parsed top-level JSON object.

        Raises:
            ConfigFileError: If the file cannot be read, is not valid
                JSON or is not a JSON object.
        """
        try:
            with config_file.open("r") as file:
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
        """Build the points settings from ``points_per``.

        Args:
            options: Parsed config file.

        Returns:
            The points settings, with defaults for invalid values.
        """
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
        """Build the list of levels from ``levels``.

        The first level defaults to a fixed seed so its maze is always
        the same; the other levels default to a random maze.

        Args:
            options: Parsed config file.

        Returns:
            One setting per level, or one default level if the list is
            missing or empty.
        """
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
                        self.FIRST_LEVEL_SEED if index == 0 else 0,
                        minimum=0,
                        where=where,
                        quiet=index != 0,
                    ),
                )
            )
        return levels

    def _build_pacman_conf(self, options: dict) -> PacManConfig:
        """Build Pac-Man's settings from ``pacman``.

        Args:
            options: Parsed config file.

        Returns:
            Pac-Man's settings.
        """
        raw = options.get("pacman")
        if not isinstance(raw, dict):
            self._warn("missing or invalid 'pacman', using defaults")

        return PacManConfig(
            dir=self.DEFAULT_PACMAN["dir"],
            next_dir=self.DEFAULT_PACMAN["next_dir"],
        )

    def load_conf(self, config_file: Path) -> None:
        """Load the config file into ``self.config``.

        Args:
            config_file: Path of the JSON config file.

        Raises:
            ConfigFileError: If the config file cannot be read.
        """
        options = self._read_options(config_file)
        self.config = Config(
            levels=self._build_levels(options),
            points=self._build_points(options),
            lives=self._get_int(
                options, "lives", self.DEFAULT_LIVES, minimum=1
            ),
            pacman=self._build_pacman_conf(options),
        )
