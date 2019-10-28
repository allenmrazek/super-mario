from abc import ABC, abstractmethod
from pygame.sprite import Rect
from enum import IntFlag
from util import copy_vector
from util import make_vector


class Layer(IntFlag):
    Background = 1 << 0     # behind blocks
    Block = 1 << 1          # layer blocks are drawn on
    Spawner = 1 << 2        # spawners go here
    Trigger = 1 << 3        # take a guess
    Mario = 1 << 4          # take a guess
    Enemy = 1 << 5          # take another guess
    Active = 1 << 6         # "active" things: think fireballs and projectiles; mario death animations
    Interface = 1 << 7      # interface stuff here
    Overlay = 1 << 8        # a final layer that absolutely will overlay everything. Use sparingly


class Entity(ABC):
    """Important note: while you can make things exist on the map by making them entities, they
    WILL NOT BE SERIALIZED. Use LevelEntity for persistent things (anything that can be placed)"""
    def __init__(self, rect: Rect):
        super().__init__()

        # reminder to self: we don't just expose this publically because we want them
        # synchronized; specifically, that position can be tracked in floating points
        # (since rects are int-only)
        self._rect = rect.copy()
        self._position = make_vector(rect.x, rect.y)  # rect only int values

    @abstractmethod
    def update(self, dt, view_rect):
        pass

    @abstractmethod
    def draw(self, screen, view_rect):
        pass

    @property
    def layer(self):
        return Layer.Background

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, val):
        self._rect = val

    @property
    def position(self):
        return copy_vector(self._position)

    @position.setter
    def position(self, pos):
        self._position = copy_vector(pos)
        self._rect.x, self._rect.y = pos

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, w):
        self._rect.width = w

    @property
    def height(self):
        return self._rect.height

    @height.setter
    def height(self, h):
        self._rect.height = h

    def get_rect(self):
        return self._rect.copy()
