from typing import TYPE_CHECKING
import pygame
from pydantic import ValidationError
import json
from src.engine.scenes.scene_baseclass import Scene
from src.models.scoreboard_models import Score

if TYPE_CHECKING:
    from src.engine.engine import Engine


class ScoreBoard(Scene):
    SCORE_FILE = "scores.json"
    TOP = 10

    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)
        self.font = pygame.font.Font("src/assets/sonicfont.ttf", 20)
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

    def draw(self, surface: pygame.surface.Surface) -> None:
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

    def _draw_10_scores(self, surface: pygame.surface.Surface) -> None:
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
        content = self._read_score_file()
        scores: list[Score] = []
        for name, value in content.items():
            try:
                scores.append(
                    Score.model_validate({"name": name, "score": value})
                )
            except ValidationError:
                print(f"{self.SCORE_FILE}: ignoring invalid entry "
                      f"{name!r}: {value!r}")

        scores.sort(key=lambda s: s.score, reverse=True)
        self.scores = {s.name: s.score for s in scores[: self.TOP]}
        self.loadscores_text()
        return self.scores

    def _read_score_file(self) -> dict[object, object]:
        try:
            with open(self.SCORE_FILE, "r") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"{self.SCORE_FILE} doesn't exist, starting with no score")
            return {}
        except OSError as e:
            print(f"Can't read {self.SCORE_FILE} ({e}), "
                  "starting with no score")
            return {}

        if not text.strip():
            return {}
        try:
            content = json.loads(text)
        except json.JSONDecodeError:
            print(f"Invalid json in {self.SCORE_FILE}, "
                  "starting with no score")
            return {}
        if not isinstance(content, dict):
            print(f"{self.SCORE_FILE} must contain a json object, "
                  "starting with no score")
            return {}
        return content

    def loadscores_text(self) -> None:
        self.fonted_scores = [
            self.font.render(f"{key}: {val}", True, (255, 255, 0))
            for key, val in self.scores.items()
        ]

    def savescore(self, score: Score) -> None:
        self.scores[score.name] = max(
            score.score, self.scores.get(score.name, 0)
        )
        self.scores = dict(
            sorted(self.scores.items(), key=lambda i: i[1], reverse=True)[
                : self.TOP
            ]
        )
        try:
            with open(self.SCORE_FILE, "w") as f:
                json.dump(self.scores, f, indent=2)
        except OSError as e:
            print(f"Can't save {self.SCORE_FILE} ({e}), "
                  "score kept for this session only")
        self.loadscores_text()
