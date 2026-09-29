import argparse
from src.engine.engine import Engine, ConfigFileError
from src.engine.scenes.scene_scoreboard import ScoreFileError


class Main:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(prog="pacman")
        parser.add_argument("configfile", nargs="?", default="config.json")
        args = parser.parse_args()
        config_file = args.configfile

        try:
            self.engine = Engine(config_file)
        except (ConfigFileError, ScoreFileError) as e:
            print(e)
            exit(1)

    def start(self) -> None:
        self.engine.run()


if __name__ == "__main__":
    main = Main()
    main.start()
