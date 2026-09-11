from pathlib import Path
import pygame

from src.engine.scenes.scene_baseclass import Scene
from src.sprites.ghost import Ghost
from src.sprites.sprites import Blinky, Pinky, Inky, Clyde
from src.sprites.pacman import PacMan


class RunningScene(Scene):
    def __init__(self, engine) -> None:
        super().__init__(engine)

        pacman_conf = self.engine.config.pacman
        lives = self.engine.config.lives

        self.pacman = PacMan(
            lives=lives,
            pos=pacman_conf.pos,
            alive=True,
            visible=True,
            dir=pacman_conf.dir,
            can_eat=False,
            next_dir=pacman_conf.next_dir,
            respawn_coord=pacman_conf.pos,
            super_power=False,
            sprite=pacman_conf.sprite,
        )

        sprite_path = Path("src/assets/ghost.png")
        raw_image = pygame.image.load(str(sprite_path)).convert_alpha()
        self.ghost_texture = pygame.transform.scale(raw_image, (32, 32))

        self.blinky = Blinky(5, 5, sprite_path)
        self.pinky = Pinky(6, 5, sprite_path)
        self.inky = Inky(7, 5, sprite_path, blinky_ref=self.blinky)
        self.clyde = Clyde(8, 5, sprite_path)

        self.ghosts: list[Ghost] = [self.blinky,
                                    self.pinky,
                                    self.inky,
                                    self.clyde]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.engine.change_scene(self.engine.scenes["Pause"])

    def update(self, dt: float) -> None:
        self.engine.wave_manager.update(dt, self.ghosts)
        pacman_pos = self.pacman.pos
        dir_vectors = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        pacman_dir = dir_vectors.get(self.pacman.dir, (0, 0))

        for ghost in self.ghosts:
            ghost.update_target(pacman_pos, pacman_dir)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))

        for ghost in self.ghosts:
            screen_x = ghost.grid_x * ghost.tile_size
            screen_y = ghost.grid_y * ghost.tile_size
            surface.blit(self.ghost_texture, (screen_x, screen_y))
