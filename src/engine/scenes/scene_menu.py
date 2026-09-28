from typing import Any
import pygame
from pygame import Surface
from src.engine.scenes.scene_baseclass import Scene


class MenuScene(Scene):
    cursor_pos_index: int = 0

    def __init__(self, engine: Any):
        super().__init__(engine)
        self.param_choice = 0
        self.cursor_pos: tuple[int, int] = (0, 0)
        self.param_list: list[tuple[str, tuple[int, int]]] = []
        self._init_fixed()
        self.font = pygame.font.Font("src/assets/sonicfont.ttf", 48)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.cursor_pos_index < len(self.param_list) - 1:
                    self.cursor_pos_index += 1
                    self.param_choice += 1
                    self.cursor_pos = (
                        self.param_list[self.cursor_pos_index][1][0] - 50,
                        self.param_list[self.cursor_pos_index][1][1] + 5,
                    )
            elif event.key == pygame.K_UP:
                if self.cursor_pos_index > 0:
                    self.cursor_pos_index -= 1
                    self.param_choice -= 1
                    self.cursor_pos = (
                        self.param_list[self.cursor_pos_index][1][0] - 50,
                        self.param_list[self.cursor_pos_index][1][1] + 5,
                    )
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.param_choice == 0:
                    running_scene = self.engine.scenes["Running"]
                    running_scene.start_new_game()
                    self.engine.change_scene(running_scene)
                elif self.param_choice == 1:
                    self.engine.change_scene(self.engine.scenes["Score"])
                elif self.param_choice == 3:
                    self.engine.running = False

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: Surface) -> None:
        self.font = pygame.font.Font("src/assets/sonicfont.ttf", 48)
        surface.fill((0, 0, 0))

        surface.blit(self.title, self.title_pos)
        surface.blit(self.play_text, self.param_list[0][1])
        surface.blit(self.score_board_text, self.param_list[1][1])
        surface.blit(self.instructions_text, self.param_list[2][1])
        surface.blit(self.quit_text, self.param_list[3][1])
        surface.blit(self.cursor, self.cursor_pos)

    def _init_fixed(self) -> None:
        self.font = pygame.font.Font("src/assets/sonicfont.ttf", 48)
        self.title = pygame.image.load(
            "src/assets/screentitle.png"
        ).convert_alpha()
        title_w = int(self.title.get_width() * 0.3)
        title_h = int(self.title.get_height() * 0.3)
        self.title = pygame.transform.scale(self.title, (title_w, title_h))

        self.cursor = pygame.image.load(
            "src/assets/cursor.png"
        ).convert_alpha()
        cursor_w = int(self.cursor.get_width() * 0.1)
        cursor_h = int(self.cursor.get_height() * 0.1)
        self.cursor = pygame.transform.scale(self.cursor, (cursor_w, cursor_h))

        self.play_text = self.font.render("PLAY", True, (250, 250, 0))
        self.score_board_text = self.font.render(
            "SCORE BOARD", True, (250, 250, 0)
        )
        self.instructions_text = self.font.render(
            "INSTRUCTIONS", True, (250, 250, 0)
        )
        self.quit_text = self.font.render("EXIT", True, (250, 250, 0))

        center_x = 800 // 2
        self.title_pos = (center_x - self.title.get_width() // 2, 0)
        self.param_list = [
            (
                "PLAY",
                (center_x - self.play_text.get_width() // 2, 500),
            ),
            (
                "SCORE BOARD",
                (center_x - self.score_board_text.get_width() // 2, 600),
            ),
            (
                "INSTRUCTIONS",
                (center_x - self.instructions_text.get_width() // 2, 700),
            ),
            (
                "EXIT",
                (center_x - self.quit_text.get_width() // 2, 800),
            ),
        ]
        self.cursor_pos = (
            self.param_list[0][1][0] - 50,
            self.param_list[0][1][1],
        )
        self.cursor_pos_index: int = 0
