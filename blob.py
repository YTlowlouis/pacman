class Blob:
    def __init__(self, lives: int,
                 position: list[int, int],
                 speed: int) -> None:
        self.lives = lives
        self.position = position
        self.speed = speed

        def info(lives, position, speed) -> None:
            print(lives)

        if Blob:
            info(3, [0, 0], 5)
