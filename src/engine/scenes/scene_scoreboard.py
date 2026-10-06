from typing import TYPE_CHECKING
import pygame
from pydantic import ValidationError
import json
from src.engine.scenes.scene_baseclass import Scene
from src.models.scoreboard_models import Score
from src.utils import get_resource_path

if TYPE_CHECKING:
    from src.engine.engine import Engine


class ScoreBoard(Scene):
    """Highscore screen; also loads and saves the top 10 scores."""

    SCORE_FILE = get_resource_path("scores.json")
    TOP = 10

    def __init__(self, engine: "Engine") -> None:
        """Load the scores and render the title.

        Args:
            engine: Game engine owning the scenes.
        """
        super().__init__(engine)
        chemin_police = get_resource_path("src/assets/sonicfont.ttf")
        self.font = pygame.font.Font(chemin_police, 36)
        self.font_title = pygame.font.Font(chemin_police, 70)
        self.scores: dict = {}
        self.loadscores()
        self.title_score_text = self.font_title.render(
            "High Scores", True, (255, 255, 0)
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        """Go back to the menu with ESC.

        Args:
            event: Pygame event to handle.
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.engine.change_scene(self.engine.scenes["Menu"])

    def update(self, dt: float) -> None:
        """Nothing to update: the screen is static.

        Args:
            dt: Elapsed time since the last frame, in seconds.
        """
        pass

    def draw(self, surface: pygame.surface.Surface) -> None:
        """Draw the title and the top 10 scores.

        Args:
            surface: Surface to draw on.
        """
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
        """Draw the 10 best scores, centered.

        Args:
            surface: Surface to draw on.
        """
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
        """Load the scores from the file, skipping invalid entries.

        Returns:
            The top 10 scores by player name, best first.
        """
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
        """Read the score file, falling back to no score on any error.

        Returns:
            The raw JSON object, or an empty dict if the file is
            missing, unreadable, not valid JSON or not an object.
        """
        try:
            with self.SCORE_FILE.open("r") as f:
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
        """Render one text surface per score."""
        self.fonted_scores = [
            self.font.render(f"{key}: {val}", True, (255, 255, 0))
            for key, val in self.scores.items()
        ]

    def savescore(self, score: Score) -> None:
        """Record a score, keep the top 10 and write them to the file.

        A player only keeps their latest score: it replaces the old one,
        even if it is lower. If the file cannot be written, the scores
        are kept for this session only.

        Args:
            score: Score to record.
        """
        self.scores[score.name] = score.score
        self.scores = dict(
            sorted(self.scores.items(), key=lambda i: i[1], reverse=True)[
                : self.TOP
            ]
        )
        try:
            with self.SCORE_FILE.open("w") as f:
                json.dump(self.scores, f, indent=2)
        except OSError as e:
            print(f"Can't save {self.SCORE_FILE} ({e}), "
                  "score kept for this session only")
        self.loadscores_text()
