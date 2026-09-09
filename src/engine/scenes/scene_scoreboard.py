from os import truncate

import pygame

import json

from src.engine.scenes.scene_baseclass import Scene


class ScoreFileError(Exception):
    pass


class ScoreBoard(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.font = pygame.font.Font(None, 43)
        self.scores: dict = {}
        self.loadscores()
        self.loadscores_text()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.engine.change_scene(self.engine.scenes["Menu"])

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))

        self._draw_10_scores(surface)

    def _draw_10_scores(self, surface: pygame.Surface) -> None:
        count = 0
        base_coords = (500, 500)
        for count, text in enumerate(self.fonted_scores):
            if count == 10:
                break
            surface.blit(
                text,
                (base_coords[0], base_coords[1] + count * 50),
            )

    def loadscores(self):
        try:
            with open("scores.json", "r") as f:
                content = json.load(f)
        except json.decoder.JSONDecodeError:
            raise ScoreFileError("Invalid json in score file")
        except FileNotFoundError:
            print("scores.json doesn't exist, creating .....")
            with open("scores.json", "w") as f:
                f.write("")
        except PermissionError:
            raise ScoreFileError("No peermission to open score file")
        except OSError as e:
            raise ScoreFileError(f"Error while loading score file: {e}")

        with open("scores.json", "r") as f:
            content = json.load(f)
            self.scores = {player: score for player, score in content.items()}
            self.scores = {
                player: score
                for player, score in sorted(
                    self.scores.items(), key=lambda item: [1]
                )
            }

    def loadscores_text(self) -> None:
        self.fonted_scores = [
            self.font.render(f"{key}: {val}", True, (255, 255, 0))
            for key, val in self.scores.items()
        ]
