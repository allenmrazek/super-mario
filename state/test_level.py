import pygame
from state.game_state import GameState
from event import EventHandler
from level import Level
import config


class TestLevel(GameState, EventHandler):
    def __init__(self, game_events, assets, level):
        super().__init__(game_events)

        self.assets = assets
        self.level = level
        self._finished = False

    def update(self, dt):
        self.level.update(dt)

    def draw(self, screen):
        screen.fill(config.default_background_color)
        self.level.draw(screen)

    @property
    def finished(self):
        return self._finished

    def activated(self):
        self.game_events.register(self)
        self.game_events.register(self.level)

    def deactivated(self):
        self.game_events.unregister(self.level)
        self.game_events.unregister(self)

    def handle_event(self, evt, game_events):
        if not self.is_consumed(evt) and evt.type == pygame.KEYDOWN and evt.key == pygame.K_q:
            self._finished = True
            self.consume(evt)
            