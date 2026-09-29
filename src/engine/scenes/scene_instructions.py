from typing import TYPE_CHECKING
import pygame

from src.engine.scenes.scene_baseclass import Scene

if TYPE_CHECKING:
    from src.engine.engine import Engine


class InstructionsScene(Scene):
    BG_COLOR = (0, 0, 0)
    TITLE_COLOR = (255, 255, 0)
    HEADER_COLOR = (255, 255, 0)
    TEXT_COLOR = (255, 255, 255)
    HINT_COLOR = (200, 200, 200)
    TITLE_Y = 40
    CONTENT_Y = 150
    LINE_GAP = 8
    SECTION_GAP = 24

    SECTIONS = [
        (
            "CONTROLS",
            [
                "Arrow keys: move",
                "ESC: pause / resume",
                "M (in pause): back to menu",
            ],
        ),
        (
            "RULES",
            [
                "Eat every pacgum to clear the level",
                "Super pacgum: ghosts flee, eat them!",
                "Touching a ghost costs a life",
                "Clear each level before time runs out",
            ],
        ),
        (
            "CHEAT MODE",
            [
                "C: enable cheats",
                "L: toggle invincibility",
                "W: skip level",
            ],
        ),
    ]

    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)
        font_title = pygame.font.Font("src/assets/sonicfont.ttf", 60)
        font_header = pygame.font.Font("src/assets/sonicfont.ttf", 32)
        font_text = pygame.font.Font("src/assets/sonicfont.ttf", 22)

        self.title = font_title.render(
            "INSTRUCTIONS", True, self.TITLE_COLOR
        )
        self.hint = font_text.render("ESC to return", True, self.HINT_COLOR)
        self.sections = [
            (
                font_header.render(header, True, self.HEADER_COLOR),
                [
                    font_text.render(line, True, self.TEXT_COLOR)
                    for line in lines
                ],
            )
            for header, lines in self.SECTIONS
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.engine.change_scene(self.engine.scenes["Menu"])

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.surface.Surface) -> None:
        surface.fill(self.BG_COLOR)
        center_x = surface.get_width() // 2

        surface.blit(
            self.title,
            (center_x - self.title.get_width() // 2, self.TITLE_Y),
        )

        y = self.CONTENT_Y
        for header, lines in self.sections:
            surface.blit(header, (center_x - header.get_width() // 2, y))
            y += header.get_height() + self.LINE_GAP
            for line in lines:
                surface.blit(line, (center_x - line.get_width() // 2, y))
                y += line.get_height() + self.LINE_GAP
            y += self.SECTION_GAP

        surface.blit(
            self.hint,
            (
                center_x - self.hint.get_width() // 2,
                surface.get_height() - self.hint.get_height() - 30,
            ),
        )
