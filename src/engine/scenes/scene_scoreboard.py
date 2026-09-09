import pygame

import json

from src.engine.scenes.scene_baseclass import Scene


class ScoreFileError(Exception):
    pass


class ScoreBoard(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        scores: dict = {}
        # self.loadscores()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.engine.change_scene(self.engine.scenes["Menu"])

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))

    def loadscores(self):
        try:
            with open("scores.json", "r") as f:
                content = json.load(f)
        except FileNotFoundError:
            print("scores.json doesn't exist, creating .....")
            with open("scores.json", "w") as f:
                f.write("")
        except PermissionError:
            raise ScoreFileError("No peermission to open score file")

        with open("scores.json", "r") as f:
            content = json.load(f)
            self.scores = {player: score for player, score in content.items()}
            self.scores = {
                player: score
                for player, score in sorted(
                    self.scores.items(), key=lambda item: [1]
                )
            }
