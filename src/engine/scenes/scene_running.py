import pygame

from src.engine.scenes.scene_baseclass import Scene


class RunningScene(Scene):
    def __init__(self):
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass
