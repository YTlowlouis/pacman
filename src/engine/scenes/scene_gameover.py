from pydantic import ValidationError
import pygame

from src.engine.scenes.scene_baseclass import Scene
from src.models.scoreboard_models import Score


class NameError(Exception):
    pass


class GameOverScene(Scene):
    TEXT_COLOR = (250, 250, 0)
    BG_COLOR = (0, 0, 0)
    NAME_MAX = 10
    TITLE_Y = 100
    FINAL_SCORE_Y = 190

    def __init__(self, engine):
        super().__init__(engine)
        self.font = pygame.font.Font("src/assets/sonicfont.ttf", 60)
        self.font_scores = pygame.font.Font("src/assets/sonicfont.ttf", 40)
        self.title_loser = self.font.render("GAME OVER", True, self.TEXT_COLOR)
        self.title_winner = self.font.render("VICTORY", True, self.TEXT_COLOR)
        self.entering_name = False
        self.player_name = ""
        self.caret_timer = 0.0
        self.final_score = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.entering_name:
            self._handle_name_input(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.engine.change_scene(self.engine.scenes["Menu"])

    #            elif event.key == pygame.K_r:
    #                running_scene = self.engine.scenes["Running"]
    #                running_scene.start_new_game()
    #                self.engine.change_scene(running_scene)

    def update(self, dt: float) -> None:
        self.caret_timer = (self.caret_timer + dt) % 1.0

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.BG_COLOR)
        center_x = surface.get_width() // 2
        if self.winner_flag is True:
            surface.blit(
                self.title_winner,
                (center_x - self.title_winner.get_width() // 2, self.TITLE_Y),
            )
        else:
            surface.blit(
                    self.title_loser,
                    (center_x - self.title_loser.get_width() // 2, self.TITLE_Y),
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
        if event.type == pygame.TEXTINPUT:
            if len(self.player_name) < self.NAME_MAX:
                self.player_name += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._validate_name()

    def _validate_name(self) -> None:
        name = self.player_name.strip() or "player"
        try:
            score = Score(name=name, score=self.final_score)
        except ValidationError:
            raise NameError(f"Invalid name: {name}, setting name to 'player'")
        self.savescore(score)
        self.scores = self.loadscore()
        self.entering_name = False

    def savescore(self, score: Score) -> None:
        self.engine.scenes["Score"].savescore(score)

    def _draw_scores(self, surface: pygame.Surface) -> None:
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
        score_scene = self.engine.scenes["Score"]
        return score_scene.loadscores()

    def enter(self, final_score: int, winner_flag: bool) -> None:
        self.final_score = final_score
        self.winner_flag = winner_flag
        self.player_name = ""
        self.entering_name = True
        self.scores = self.loadscore()
