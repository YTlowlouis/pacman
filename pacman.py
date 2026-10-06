import argparse
import sys
from pathlib import Path

import pygame

from src.engine.engine import Engine, ConfigFileError
from src.engine.scenes.scene_running import MazeGenerationError
from src.utils import get_resource_path


class Main:
    """Command-line entry point: parses arguments and runs the game."""

    def __init__(self) -> None:
        """Parse the command line and build the game engine.

        Exactly one argument, the config file, is expected. The packaged
        game is launched without arguments, so it falls back to the
        bundled config file.

        Exits with status 1 and a clear message if the configuration
        file, the first maze or an asset cannot be loaded.
        """
        parser = argparse.ArgumentParser(prog="pacman")
        if getattr(sys, "frozen", False):
            parser.add_argument(
                "configfile",
                nargs="?",
                default=str(get_resource_path("config.json")),
            )
        else:
            parser.add_argument("configfile", help="JSON config file")
        args = parser.parse_args()
        config_file = Path(args.configfile)

        if not config_file.is_file():
            print(f"Error: {config_file} is not an existing file")
            sys.exit(1)

        try:
            self.engine = Engine(config_file)
        except (ConfigFileError, MazeGenerationError) as e:
            print(e)
            sys.exit(1)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Error: missing or invalid asset: {e}")
            pygame.quit()
            sys.exit(1)

    def start(self) -> None:
        """Run the game loop until the window is closed.

        Exits with status 1 and a clear message if a maze or an asset
        cannot be loaded during the game.
        """
        try:
            self.engine.run()
        except MazeGenerationError as e:
            print(e)
            sys.exit(1)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Error: missing or invalid asset: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main = Main()
    main.start()
