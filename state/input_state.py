import sys
import pygame
from pygame.locals import *


class InputState:
    def __init__(self):
        self.left, self.right, self.up, self.down, self.fire = False, False, False, False, False
        self.quit = False

        self.left_down = False
        self.mouse_pos = (0, 0)

        self.key_actions = {
            K_ESCAPE: self.__quit,
            K_LEFT: self.__left,
            K_RIGHT: self.__right,
            K_UP: self.__up,
            K_DOWN: self.__down
        }

        self.key_codes = []

    def __quit(self, state):
        self.quit = state

    def __left(self, state):
        self.left = state

    def __right(self, state):
        self.right = state

    def __up(self, state):
        self.up = state

    def __down(self, state):
        self.down = state

    def do_events(self):
        self.key_codes.clear()
        self.mouse_pos = pygame.mouse.get_pos()

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if evt.type == KEYDOWN or evt.type == KEYUP:
                    state = True if evt.type == pygame.KEYDOWN else False

                    if state:
                        self._handle_text_entry(evt.key)

                    if evt.key in self.key_actions:
                        action = self.key_actions[evt.key]

                        if action is not None:
                            action(state)

                elif evt.type == MOUSEBUTTONDOWN:
                    self.left_down = True
                elif evt.type == MOUSEBUTTONUP:
                    self.left_down = False

    def _handle_text_entry(self, key):
        alpha = K_a <= key <= K_z
        digit = not alpha and K_0 <= key <= K_9

        if alpha or digit or key in [K_SPACE, K_BACKSPACE, K_RETURN, K_KP_ENTER]:
            upper = pygame.key.get_mods() & KMOD_SHIFT
            key = key & ~0x20 if alpha and upper else key

            self.key_codes.append(key)
