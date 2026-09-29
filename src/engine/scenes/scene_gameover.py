from typing import TYPE_CHECKING
from pydantic import ValidationError
import pygame

from src.engine.scenes.scene_baseclass import Scene
from src.engine.scenes.scene_scoreboard import ScoreBoard
from src.models.scoreboard_models import Score

if TYPE_CHECKING:
    from src.engine.engine import Engine


class GameOverScene(Scene):
    """End screen, for both defeat and victory.

    Shows the final score and asks for the player's name, then
    shows the highscores.
    """

    TEXT_COLOR = (250, 250, 0)
    BG_COLOR = (0, 0, 0)
    NAME_MAX = 10
    TITLE_Y = 100
    FINAL_SCORE_Y = 190

    def __init__(self, engine: "Engine") -> None:
        """Render the titles.

        Args:
            engine: Game engine owning the scenes.
        """
        super().__init__(engine)
        self.font = pygame.font.Font("src/assets/sonicfont.ttf", 60)
        self.font_scores = pygame.font.Font("src/assets/sonicfont.ttf", 40)
        self.title_loser = self.font.render("GAME OVER", True, self.TEXT_COLOR)
        self.title_winner = self.font.render("VICTORY", True, self.TEXT_COLOR)

        self.entering_name = False
        self.player_name = ""
        self.caret_timer = 0.0
        self.final_score = 0
        self.winner_flag = False

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle name typing, or go back to the menu with ESC.

        Args:
            event: Pygame event to handle.
        """
        if self.entering_name:
            self._handle_name_input(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.engine.change_scene(self.engine.scenes["Menu"])

    def update(self, dt: float) -> None:
        """Blink the text caret.

        Args:
            dt: Elapsed time since the last frame, in seconds.
        """
        self.caret_timer = (self.caret_timer + dt) % 1.0

    def draw(self, surface: pygame.surface.Surface) -> None:
        """Draw the title, the final score and the name prompt or the
        highscores.

        Args:
            surface: Surface to draw on.
        """
        surface.fill(self.BG_COLOR)
        center_x = surface.get_width() // 2
        title = self.title_winner if self.winner_flag else self.title_loser
        surface.blit(
            title,
            (center_x - title.get_width() // 2, self.TITLE_Y),
        )
        final = self.font_scores.render(
            f"Your score: {self.final_score}", True, self.TEXT_COLOR
        )
        surface.blit(
            final, (center_x - final.get_width() // 2, self.FINAL_SCORE_Y)
        )

        if self.entering_name:
            caret = "_" if self.caret_timer < 0.5 else " "
            prompt = self.font_scores.render(
                f"Name: {self.player_name}{caret}", True, self.TEXT_COLOR
            )
            surface.blit(
                prompt,
                (surface.get_width() // 2 - prompt.get_width() // 2, 700),
            )
        else:
            self._draw_scores(surface)

    def _handle_name_input(self, event: pygame.event.Event) -> None:
        """Type the name: letters, digits and spaces only, 10 at most.

        Backspace erases a character and Enter validates the name.

        Args:
            event: Pygame event to handle.
        """
        if event.type == pygame.TEXTINPUT:
            for char in event.text:
                if len(self.player_name) >= self.NAME_MAX:
                    break
                if char.isalnum() or char == " ":
                    self.player_name += char
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._validate_name()

    def _validate_name(self) -> None:
        """Save the score under the typed name.

        An empty or invalid name is replaced by 'player'.
        """
        name = self.player_name.strip() or "player"
        try:
            score = Score(name=name, score=self.final_score)
        except ValidationError:
            print(f"Invalid name: {name}, setting name to 'player'")
            score = Score(name="player", score=self.final_score)
        self.savescore(score)
        self.scores = self.loadscore()
        self.entering_name = False

    def savescore(self, score: Score) -> None:
        """Save a score through the scoreboard scene.

        Args:
            score: Score to save.
        """
        score_scene = self.engine.scenes["Score"]
        if isinstance(score_scene, ScoreBoard):
            score_scene.savescore(score)

    def _draw_scores(self, surface: pygame.surface.Surface) -> None:
        """Draw the 10 best scores, centered.

        Args:
            surface: Surface to draw on.
        """
        center_x = surface.get_width() // 2
        base_y = 250

        fonted_scores = [
            self.font_scores.render(f"{key}: {val}", True, (255, 255, 0))
            for key, val in self.scores.items()
        ]

        for x, score in enumerate(fonted_scores):
            if x == 10:
                break
            surface.blit(
                score,
                (center_x - score.get_width() // 2, base_y + x * 50),
            )

    def loadscore(self) -> dict[str, int]:
        """Load the scores through the scoreboard scene.

        Returns:
            The top 10 scores by player name.
        """
        score_scene = self.engine.scenes["Score"]
        if isinstance(score_scene, ScoreBoard):
            return score_scene.loadscores()
        return {}

    def enter(self, final_score: int, winner_flag: bool) -> None:
        """Prepare the screen for a finished game.

        Args:
            final_score: Score reached by the player.
            winner_flag: True if every level was cleared.
        """
        self.final_score = final_score
        self.winner_flag = winner_flag
        self.player_name = ""
        self.entering_name = True
        self.scores = self.loadscore()
