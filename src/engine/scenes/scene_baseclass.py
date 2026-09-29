import pygame
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine.engine import Engine


class Scene(ABC):
    """Base class of every screen of the game."""

    def __init__(self, engine: "Engine"):
        """Keep a reference to the engine.

        Args:
            engine: Game engine owning the scenes.
        """
        self.engine = engine

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle one input event.

        Args:
            event: Pygame event to handle.
        """

    @abstractmethod
    def update(self, dt: float) -> None:
        """Advance the scene by one frame.

        Args:
            dt: Elapsed time since the last frame, in seconds.
        """

    @abstractmethod
    def draw(self, surface: pygame.surface.Surface) -> None:
        """Draw the scene.

        Args:
            surface: Surface to draw on.
        """
