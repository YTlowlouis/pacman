import pygame
from src.engine.scenes.scene_baseclass import Scene


class PauseScene(Scene):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        self.font_title = pygame.font.Font(None, 74)
        self.font_text = pygame.font.Font(None, 36)

        self.title_surface = self.font_title.render("PAUSED",
                                                    True, (255, 255, 0))
        self.resume_text = self.font_text.render("Press ESC to Resume",
                                                 True, (255, 255, 255))
        self.menu_text = self.font_text.render("Press M for Main Menu",
                                               True, (200, 200, 200))

        self.background_snapshot: pygame.Surface | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.engine.change_scene(self.engine.scenes["Running"])
            elif event.key == pygame.K_m:
                self.engine.change_scene(self.engine.scenes["Menu"])

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if self.background_snapshot:
            surface.blit(self.background_snapshot, (0, 0))

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2

        title_pos = (center_x - self.title_surface.get_width() // 2,
                     center_y - 100)
        resume_pos = (center_x - self.resume_text.get_width() // 2,
                      center_y + 20)
        menu_pos = (center_x - self.menu_text.get_width() // 2,
                    center_y + 70)

        surface.blit(self.title_surface, title_pos)
        surface.blit(self.resume_text, resume_pos)
        surface.blit(self.menu_text, menu_pos)
