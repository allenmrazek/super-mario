from abc import ABC, abstractmethod
from pygame.sprite import Rect
from enum import IntFlag
from util import copy_vector
from util import make_vector





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
