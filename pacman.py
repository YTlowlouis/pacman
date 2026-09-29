import argparse
from src.engine.engine import Engine, ConfigFileError


class Main:
    """Command-line entry point: parses arguments and runs the game."""

    def __init__(self) -> None:
        """Parse the command line and build the game engine.

        Exits with status 1 and a clear message if the configuration
        file cannot be loaded.
        """
        parser = argparse.ArgumentParser(prog="pacman")
        parser.add_argument("configfile", nargs="?", default="config.json")
        args = parser.parse_args()
        config_file = args.configfile

        try:
            self.engine = Engine(config_file)
        except ConfigFileError as e:
            print(e)
            exit(1)

    def start(self) -> None:
        """Run the game loop until the window is closed."""
        self.engine.run()


if __name__ == "__main__":
    main = Main()
    main.start()
