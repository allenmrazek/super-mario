import pygame
from state.game_state import GameState
from entities.entity_manager import EntityManager
from assets.level import Level
from assets.statistics import Statistics
from event.game_events import EventHandler
from .game_state import state_stack
from scoring import Labels


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
        return self._finished or self.level.cleared or self.stats.lives <= 0

    def activated(self):
        self.game_events.register(self.level)

    def deactivated(self):
        self.game_events.unregister(self.level)

    @staticmethod
    def run(assets, level_filename):
        level = Level(assets, EntityManager.create_default())

        level.load_from_path(level_filename)

        return RunLevel(None, assets, level, Statistics(Labels()))
