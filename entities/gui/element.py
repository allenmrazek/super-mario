from enum import Enum
from abc import abstractmethod
import pygame
from entities.entity import Entity
from entities.entity import Layer
from event import EventHandler
from util import copy_vector


class Anchor(Enum):
    CENTER = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4


class Element(Entity, EventHandler):
    _element_position_setters = {}

    def __init__(self, element_position, anchor=Anchor.CENTER, initial_rect=None):
        super().__init__(initial_rect or pygame.Rect(0, 0, 0, 0))

        self.anchor = anchor
        self.element_position = copy_vector(element_position)
        self.position = self.element_position

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @property
    def layer(self):
        return Layer.Interface

    def update_element_position(self):
        # update position based on anchor
        Element._element_position_setters[self.anchor](self)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_pos):
        self.element_position = copy_vector(new_pos)
        self.update_element_position()

    @staticmethod
    def set_center(element):
        element.x = element.element_position.x - element.width // 2
        element.y = element.element_position.y - element.height // 2

    @staticmethod
    def set_top_left(element):
        element.x, element.y = element.element_position

    @staticmethod
    def set_top_right(element):
        tp = element.element_position

        element.x, element.y = tp.x - element.width, tp.y

    @staticmethod
    def set_bottom_left(element):
        tp = element.element_position

        element.x, element.y = tp.x, tp.y - element.height

    @staticmethod
    def set_bottom_right(element):
        tp = element.element_position

        element.x = tp.x - element.width
        element.y = tp.y - element.height


Element._element_position_setters = {Anchor.CENTER: Element.set_center,
                                     Anchor.TOP_LEFT: Element.set_top_left,
                                     Anchor.TOP_RIGHT: Element.set_top_right,
                                     Anchor.BOTTOM_LEFT: Element.set_bottom_left,
                                     Anchor.BOTTOM_RIGHT: Element.set_bottom_right}
