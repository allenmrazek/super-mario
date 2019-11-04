import pygame
from .game_state import GameState
from scoring import Labels
import config
from util import make_vector
from event import EventHandler


class TimeOut(GameState, EventHandler):
    DURATION = 3.

    def __init__(self, game_events, stats, scoring_labels):
        super().__init__(game_events)

        self.scoring_labels = scoring_labels

        self._finished = False
        self.game_over = Labels.font.render("TIME", True, pygame.Color('white'))
        self.game_over_pos = make_vector(*config.screen_rect.center) - make_vector(self.game_over.get_width() // 2,
                                                                                   self.game_over.get_height() // 2)
        pygame.mixer_music.stop()

        self._time_left = TimeOut.DURATION

    def update(self, dt):
        self._time_left -= dt

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.scoring_labels.show_labels(screen)
        screen.blit(self.game_over, self.game_over_pos)

    @property
    def finished(self):
        return self._time_left <= 0.

    def activated(self):
        pass

    def deactivated(self):
        pass

    def handle_event(self, evt, game_events):
        pass
