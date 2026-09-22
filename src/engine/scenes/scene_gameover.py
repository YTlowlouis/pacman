import pygame

from src.engine.scenes.scene_baseclass import Scene


class GameOverScene(Scene):
    TEXT_COLOR = (250, 250, 0)
    BG_COLOR = (0, 0, 0)

    def __init__(self, engine):
        super().__init__(engine)
        self.font = pygame.font.Font("src/assets/sonicfont.ttf", 60)
        self.font_scores = pygame.font.Font("src/assets/sonicfont.ttf", 40)
        self.title = self.font.render("GAME OVER", True, self.TEXT_COLOR)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.engine.change_scene(self.engine.scenes["Menu"])
            elif event.key == pygame.K_r:
                running_scene = self.engine.scenes["Running"]
                running_scene.start_new_game()
                self.engine.change_scene(running_scene)

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.BG_COLOR)
        surface.blit(
            self.title,
            (
                surface.get_width() // 2 - self.title.get_width() // 2,
                100,
            ),
        )
        self._draw_scores(surface)

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

    def enter(self, final_score: int) -> None:
        self.scores = self.loadscore()
        self.final_score = final_score
