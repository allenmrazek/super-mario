from .game_state import GameState
from level import Level
import config


class TestLevel(GameState):
    def __init__(self, game_events, atlas):
        super().__init__(game_events)

        self.atlas = atlas
        self.level = Level.create_default(atlas)

    def update(self, dt):
        self.level.update(dt)

    def draw(self, screen):
        screen.fill(config.default_background_color)
        self.level.draw(screen)

    @property
    def finished(self):
        return False

    def activated(self):
        self.game_events.register(self.level)

    def deactivated(self):
        self.game_events.unregister(self.level)
