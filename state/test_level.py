from .game_state import GameState
import config


class TestLevel(GameState):
    def __init__(self, game_events, atlas):
        super().__init__(game_events)

        self.atlas = atlas

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(config.default_background_color)

    @property
    def finished(self):
        return False
