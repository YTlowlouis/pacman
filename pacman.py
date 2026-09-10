from src.engine.engine import Engine, ConfigFileError
from src.engine.scenes.scene_scoreboard import ScoreFileError
import argparse


class Main:
    def __init__(self):
        parser = argparse.ArgumentParser(prog="pacman")
        parser.add_argument("configfile", default="config.json")
        args = parser.parse_args()
        config_file = args.configfile

        try:
            engine = Engine(config_file)
            engine.run()
        except ConfigFileError as e:
            print(e)
        except ScoreFileError as e:
            print(e)

        engine.run()


if __name__ == "__main__":
    main = Main()
