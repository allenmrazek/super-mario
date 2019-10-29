import pygame
from state.game_state import GameState, state_stack
from event import EventHandler
from assets.level import Level
from entities.entity_manager import EntityManager
from assets.statistics import Statistics


class RunLevel(GameState, EventHandler):
    def __init__(self, game_events, assets, level):
        super().__init__(game_events)

        self.stats = Statistics()
        self.assets = assets
        self.level = level
        self._finished = False

    def update(self, dt):
        self.level.update(dt)

    def draw(self, screen):
        screen.fill(self.level.background_color)
        self.level.draw(screen)

    def advance_next_level(self, level_filename):
        new_level = Level(self.assets, EntityManager.create_default())
        new_level.load_from_path(level_filename)

        self.level = new_level
        # todo: "overlay" screen for new level

    @property
    def finished(self):
        return self._finished

    def activated(self):
        self.game_events.register(self)
        self.game_events.register(self.level)

        pygame.mixer_music.load("sounds/music/01-main-theme-overworld.ogg")
        pygame.mixer_music.play()

    def deactivated(self):
        self.game_events.unregister(self.level)
        self.game_events.unregister(self)

    def handle_event(self, evt, game_events):
        if not self.is_consumed(evt) and evt.type == pygame.KEYDOWN and evt.key in [pygame.K_q, pygame.K_ESCAPE]:
            self._finished = True
            self.consume(evt)

    @staticmethod
    def run(assets, level_filename):
        level = Level(assets, EntityManager.create_default())

        level.load_from_path(level_filename)

        return RunLevel(None, assets, level)
