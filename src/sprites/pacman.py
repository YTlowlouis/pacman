class PacMan:
    def __init__(self, lives: int,
                 pos: list[int, int],
                 alive: bool,
                 dir: str,
                 next_dir: str,
                 points: int,
                 respawn_coord: list[int, int],
                 super_power: bool,
                 ) -> None:
        self.lives: int = 3
        self.pos = pos
        self.alive: bool = True
        self.dir = dir
        self.next_dir = next_dir
        self.points: int = 0
        self.respawn_coord = self.respawn_coord
        self.super_power: bool = False

        VALID_DIRECTIONS = {"up", "down", "right",
                            "left"}
        
        if lives == 0:
            alive = False
        
""" Can move through corridors only (no walls).
• Can move in 4 directions (up, down, left, right) using arrow keys or WASD (de-
pending on your keyboard).
• Starts with 3 lives.
• Loses a life when touched by a ghost.
• Respawns in the middle of the maze after losing a life.
• Game over when all lives are lost.
• Wins the level when all pacgums are eaten.
• Wins the game when all levels are completed.
• Eating a pacgum increases the score by X points.
• Eating a super-pacgum (power pellet) increases the score by Y points and makes
ghosts edible for a short time.
• Eating an edible ghost increases the score by Z points. """