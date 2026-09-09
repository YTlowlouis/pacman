import pygame
import json

from src.engine.scenes.scene_baseclass import Scene


class ScoreFileError(Exception):
    pass


class ScoreBoard(Scene):
    def __init__(self, engine):
        super().__init__(engine)

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def loadscores(self):
        try:
            with open("scores.json", "r") as f:
                content = json.load(f)
                pass
        except FileNotFoundError:
            print("scores.json doesn't exist, creating .....")
            with open("scores.json", "w") as f:
                f.write("")
        except PermissionError:
            raise ScoreFileError("No peermission to open score file")

        with open("scores.json", "r") as f:
            content = json.load(f)
            scores = {player: score for player, score in content.items()}
            sorted(
                scores,
            )
