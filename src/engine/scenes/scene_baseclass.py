import pygame
from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...
