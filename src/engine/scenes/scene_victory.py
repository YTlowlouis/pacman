import pygame

from src.engine.scenes.scene_baseclass import Scene


class Victory(Scene):
    BG_COLOR = (0, 0, 0)
    TEXT_COLOR = (255, 255, 0)

    def __init__(self, engine):
        super().__init__(engine)
        self.font_title = pygame.font.Font("src/assets/sonicfont.ttf", 70)
        self.font_hint = pygame.font.Font("src/assets/sonicfont.ttf", 40)
        self.title_win_text = self.font_title.render(
            "Win", True, self.TEXT_COLOR
        )
        self.hint_text = self.font_hint.render(
            "M to return to menu", True, self.TEXT_COLOR
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.engine.change_scene(self.engine.scenes["Menu"])

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.BG_COLOR)
        surface.blit(
            self.title_win_text,
            (
                surface.get_width() // 2
                - self.title_win_text.get_width() // 2,
                100,
            ),
        )
        surface.blit(
            self.hint_text,
            (
                surface.get_width() // 2 - self.hint_text.get_width() // 2,
                surface.get_height() - 150,
            ),
        )
