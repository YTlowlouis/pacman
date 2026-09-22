import pygame
from pydantic import ValidationError
import json
from src.engine.scenes.scene_baseclass import Scene
from src.models.scoreboard_models import Score


class ScoreFileError(Exception):
    pass


class ScoreBoard(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.font = pygame.font.Font(None, 43)
        self.font_title = pygame.font.Font(None, 70)
        self.scores: dict = {}
        self.loadscores()
        self.title_score_text = self.font_title.render(
            "High Scores", True, (255, 255, 0)
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.engine.change_scene(self.engine.scenes["Menu"])

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))

        surface.blit(
            self.title_score_text,
            (
                surface.get_width() // 2
                - self.title_score_text.get_width() // 2,
                100,
            ),
        )
        self._draw_10_scores(surface)

    def _draw_10_scores(self, surface: pygame.Surface) -> None:
        center_x = surface.get_width() // 2
        base_y = 200
        for count, text in enumerate(self.fonted_scores):
            if count == 10:
                break
            surface.blit(
                text,
                (center_x - text.get_width() // 2, base_y + count * 50),
            )

    def loadscores(self) -> dict[str, int]:
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
            try:
                for player, score in self.scores.items():
                    score = Score(name=player, score=score)
            except ValidationError as e:
                raise ScoreFileError(e)

            self.scores = {
                player: score
                for player, score in sorted(
                    self.scores.items(), key=lambda item: item[1], reverse=True
                )
            }
        self.loadscores_text()
        return self.scores

    def loadscores_text(self) -> None:
        self.fonted_scores = [
            self.font.render(f"{key}: {val}", True, (255, 255, 0))
            for key, val in self.scores.items()
        ]
