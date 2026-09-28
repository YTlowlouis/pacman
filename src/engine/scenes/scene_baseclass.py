from pygame import Surface
import pygame
from abc import ABC, abstractmethod
from typing import Any
""" from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.engine.engine_core import Engine """


class Scene(ABC):
    def __init__(self, engine: Any):
        self.engine: Any = engine

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def draw(self, surface: Surface) -> None: ...

    def savescore(self, score: Any) -> None:
        pass

    def loadscores(self) -> dict[str, int]:
        return {}
