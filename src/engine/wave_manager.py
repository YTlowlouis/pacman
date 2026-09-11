from src.sprites.ghost import GhostState, Ghost


class WaveManager:
    def __init__(self) -> None:
        self.waves = [
            (GhostState.SCATTER, 7),
            (GhostState.CHASE, 20),
            (GhostState.SCATTER, 7),
            (GhostState.CHASE, 20),
            (GhostState.SCATTER, 5),
            (GhostState.CHASE, 20),
            (GhostState.SCATTER, 5),
            (GhostState.CHASE, float('inf'))
        ]
        self.current_wave_index = 0
        self.timer = 0.0
        self.current_state = self.waves[self.current_wave_index][0]

    def update(self, dt: float, ghosts: list[Ghost]) -> None:
        if any(g.state == GhostState.FRIGHTENED for g in ghosts):
            return

        current_wave_state, wave_duration = self.waves[self.current_wave_index]
        self.timer += dt

        if self.timer >= wave_duration:
            self.timer = 0.0
            self.current_wave_index += 1

            if self.current_wave_index < len(self.waves):
                self.current_state = self.waves[self.current_wave_index][0]
                self._apply_state_to_ghosts(ghosts)

    def _apply_state_to_ghosts(self, ghosts: list[Ghost]) -> None:
        for ghost in ghosts:
            if ghost.state in (GhostState.SCATTER, GhostState.CHASE):
                ghost.state = self.current_state
