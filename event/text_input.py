from pygame.locals import *
import pygame
from .game_events import EventHandler


class TextInputHandler(EventHandler):
    string: str

    def __init__(self, initial_text=""):
        super().__init__()
        self.string = initial_text or ""

    def handle_event(self, evt, game_events):
        if evt.type == KEYDOWN and not EventHandler.is_consumed(evt):
            key = evt.key

            alpha = K_a <= key <= K_z
            digit = not alpha and (K_0 <= key <= K_9)

            if K_KP0 <= key <= K_KP9:
                digit = True
                key -= 0xD0

            if alpha:
                upper = pygame.key.get_mods() & KMOD_SHIFT
                key = key & ~0x20 if alpha and upper else key

                self.string += chr(key)

                EventHandler.consume(evt)

            elif digit:
                self.string += chr(key)
                EventHandler.consume(evt)

            elif key in [K_SPACE, K_BACKSPACE]:
                if key == K_BACKSPACE:
                    self.string = self.string[0:-1]
                else:
                    self.string += chr(key)

                EventHandler.consume(evt)

            else:  # could be things like ,/" etc
                if chr(key) in '._':
                    self.consume(evt)
                    self.string += chr(key)

                pass
