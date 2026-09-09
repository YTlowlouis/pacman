from src.engine.engine import Engine, ConfigFileError
import argparse


class Main:
    def __init__(self):
        try:
            parser = argparse.ArgumentParser(prog="pacman")
            parser.add_argument("configfile", default="config.json")
            args = parser.parse_args()
            config_file = args.configfile
        except Exception:
            print("Erreur")

        try:
            engine = Engine(config_file)
        except ConfigFileError as e:
            print(e)

        try:
            engine.run()
        except Exception:
            print("test")


if __name__ == "__main__":
    main = Main()
