import pygame
from .game_state import GameState
from event import GameEvents, EventHandler
from scoring import Labels
import config
from util import make_vector


class GameOver(GameState, EventHandler):
    def __init__(self, scoring_labels):
        super().__init__(GameEvents())

        self.scoring_labels = scoring_labels

        self._finished = False
        self.game_over = Labels.font.render("Game Over", True, pygame.Color('white'))
        self.game_over_pos = make_vector(*config.screen_rect.center) - make_vector(self.game_over.get_width() // 2,
                                                                                   self.game_over.get_height() // 2)

        # play game over music
        pygame.mixer_music.load('sounds/music/smb_gameover.wav')
        pygame.mixer_music.set_endevent(pygame.USEREVENT)
        pygame.mixer_music.play()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.scoring_labels.show_labels(screen)
        screen.blit(self.game_over, self.game_over_pos)

    @property
    def finished(self):
        return self._finished

    def activated(self):
        self.game_events.register(self)

    def deactivated(self):
        self.game_events.unregister(self)
        pygame.mixer_music.set_endevent()

    def handle_event(self, evt, game_events):
        if evt.type == pygame.USEREVENT:
            self._finished = True
        elif evt.type == pygame.QUIT:
            exit()
