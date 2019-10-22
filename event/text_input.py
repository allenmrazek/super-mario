from pygame.locals import *
import pygame
from .game_events import EventHandler


class TextInputHandler(EventHandler):
    string: str

    def __init__(self):
        super().__init__()
        self.string = ""

    def handle_event(self, evt, game_events):
        if evt.type == KEYDOWN and not EventHandler.is_consumed(evt):
            key = evt.key

            alpha = K_a <= key <= K_z
            digit = not alpha and K_0 <= key <= K_9

            if alpha:
                upper = pygame.key.get_mods() & KMOD_SHIFT
                key = key & ~0x20 if alpha and upper else key
                self.string += chr(key)
                EventHandler.consume(evt)
            elif digit:
                self.string += chr(key)
                EventHandler.consume(evt)
            elif key in [K_SPACE, K_BACKSPACE, K_RETURN, K_KP_ENTER]:
                if key == K_BACKSPACE:
                    self.string = self.string[0:-1]
                else:
                    self.string += chr(key)

                EventHandler.consume(evt)
            else:  # could be things like ,/" etc
                # todo
                pass
