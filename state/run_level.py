from state.game_state import GameState
from .time_over import TimeOut
from . import state_stack


class RunLevel(GameState):
    def __init__(self, game_events, assets, level, stats):
        super().__init__(game_events)

        self.stats = stats
        self.assets = assets
        self.level = level
        self._finished = False

    def update(self, dt):
        self.level.update(dt)
        self.stats.update(dt)

    def draw(self, screen):
        screen.fill(self.level.background_color)
        self.level.draw(screen)

    @property
    def finished(self):
        return self._finished or self.level.cleared or self.stats.lives <= 0 or self.level.timed_out

    def activated(self):
        self.game_events.register(self.level)

    def deactivated(self):
        self.game_events.unregister(self.level)
