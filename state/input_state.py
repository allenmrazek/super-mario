import sys
import pygame
from pygame.locals import *


class InputState:
    def __init__(self):
        self.left, self.right, self.up, self.down = False, False, False, False
        self.fire, self.dash, self.jump = False, False, False
        self.quit = False

        self.left_down = False
        self.mouse_pos = (0, 0)

        self.key_actions = {
            K_ESCAPE: self._quit,
            K_LEFT: self._left,
            K_RIGHT: self._right,
            K_UP: self._up,
            K_DOWN: self._down,
            K_SPACE: self._jump,
            KMOD_LSHIFT: self._dash,
            K_z: self._jump,
            K_x: self._dash
        }

        self.key_codes = []

    def _quit(self, state):
        self.quit = state

    def _left(self, state):
        self.left = state

    def _right(self, state):
        self.right = state

    def _up(self, state):
        self.up = state

    def _down(self, state):
        self.down = state

    def _jump(self, state):
        self.jump = state

    def _dash(self, state):
        self.dash = state
        self.fire = state

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

        # pygame doesn't seem to have an event for only shift
        self.dash = (pygame.key.get_mods() & KMOD_SHIFT)

    def _handle_text_entry(self, key):
        alpha = K_a <= key <= K_z
        digit = not alpha and K_0 <= key <= K_9

        if alpha or digit or key in [K_SPACE, K_BACKSPACE, K_RETURN, K_KP_ENTER]:
            upper = pygame.key.get_mods() & KMOD_SHIFT
            key = key & ~0x20 if alpha and upper else key

            self.key_codes.append(key)
