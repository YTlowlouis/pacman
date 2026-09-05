from src.engine.engine import Engine, ConfigFileError
import argparse


class Main:
    def __init__(self):
        parser = argparse.ArgumentParser(prog="pacman")
        parser.add_argument("configfile", default="config.json")
        args = parser.parse_args()
        config_file = args.configfile

        try:
            engine = Engine(config_file)
        except ConfigFileError as e:
            print(e)

        engine.run()


if __name__ == "__main__":
    main = Main()
