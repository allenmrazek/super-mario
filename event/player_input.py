import pygame
from pygame.locals import *
from .game_events import EventHandler


class PlayerInputHandler(EventHandler):
    __slots__ = ['left', 'right', 'up', 'down', 'jump', 'dash', 'quit', 'fire',
                 'left_click', 'right_click', 'mouse_position']

    def __init__(self):
        super().__init__()

        self.left, self.right, self.up, self.down = False, False, False, False
        self.jump, self.dash, self.fire = False, False, False
        self.left_click, self.right_click = False, False
        self.mouse_position = pygame.mouse.get_pos()
        self.quit = False

        self._key_actions = {
            K_ESCAPE: self._quit,
            K_LEFT: self._left,
            K_RIGHT: self._right,
            K_UP: self._up,
            K_DOWN: self._down,
            K_SPACE: self._jump,
            K_z: self._jump,
            K_x: self._dash,
            304: self._dash  # left shift
        }

    def handle_event(self, evt, game_events):
        if not EventHandler.is_consumed(evt) and (evt.type == KEYDOWN or evt.type == KEYUP):
            state = True if evt.type == KEYDOWN else False
            key = evt.key

            if key in self._key_actions:
                self._key_actions[key](state)
                EventHandler.consume(evt)

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
