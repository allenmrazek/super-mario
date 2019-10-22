from enum import Enum
import pygame
from entities.entity import Entity
from entities.entity import Layer
from event import EventHandler
from util import make_vector
from util import copy_vector


class Anchor(Enum):
    CENTER = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4


class Element(Entity, EventHandler):
    _element_position_setters = {}

    def __init__(self, position, anchor=Anchor.CENTER, initial_rect=None):
        super().__init__(initial_rect or pygame.Rect(position[0], position[1], 0, 0))

        self.anchor = anchor
        self.parent = None
        self.children = []
        self.relative_position = copy_vector(position)
        self.position = self.relative_position

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self, screen):
        for child in self.children:
            child.draw(screen)

    @property
    def layer(self):
        return Layer.Interface

    def handle_event(self, evt, game_events):
        # give children a chance to handle events
        for child in self.children:
            if hasattr(child, "handle_event"):
                child.handle_event(evt, game_events)
                if evt.consumed:
                    break

    def layout(self):
        # update position based on anchor
        Element._element_position_setters[self.anchor](self)

        # children dependent on our position
        for child in self.children:
            child.layout()

    def add_child(self, ui_element):
        assert isinstance(ui_element, Element)

        if ui_element not in self.children:
            self.children.append(ui_element)
            ui_element.parent = self
            ui_element.layout()

    def remove_child(self, ui_element):
        assert hasattr(ui_element, "parent") and ui_element.parent is self

        self.children.remove(ui_element)
        ui_element.parent = None

    def bring_to_front(self, child_element):
        if child_element in self.children and self.children[len(self.children) - 1] is not child_element:
            self.children.remove(child_element)
            self.children.append(child_element)

    def send_to_back(self, child_element):
        if child_element in self.children and self.children[0] is not child_element:
            self.children.remove(child_element)
            self.children.insert(0, child_element)

    def get_absolute_position(self):
        return self.relative_position + (self.parent.get_absolute_position()
                                         if self.parent is not None else pygame.Vector2())

    def get_absolute_rect(self):
        pos = self.get_absolute_position()

        return pygame.Rect(pos.x, pos.y, self.width, self.height)

    @staticmethod
    def set_center(element):
        if element.parent is None:
            element.position = make_vector(element.relative_position.x - element.width // 2,
                                           element.relative_position.y - element.height // 2)
        else:
            absolute_position = element.parent.get_absolute_position() + element.relative_position
            absolute_position.x -= element.width // 2
            absolute_position.y -= element.height // 2

            element.position = absolute_position

    @staticmethod
    def set_top_left(element):
        element.position = element.get_absolute_position()

    @staticmethod
    def set_top_right(element):
        element.position = element.get_absolute_position() - make_vector(element.width, 0)

    @staticmethod
    def set_bottom_left(element):
        element.position = element.get_absolute_position() - make_vector(0, element.height)

    @staticmethod
    def set_bottom_right(element):
        element.position = element.get_absolute_position() - make_vector(element.width, element.height)


Element._element_position_setters = {Anchor.CENTER: Element.set_center,
                                     Anchor.TOP_LEFT: Element.set_top_left,
                                     Anchor.TOP_RIGHT: Element.set_top_right,
                                     Anchor.BOTTOM_LEFT: Element.set_bottom_left,
                                     Anchor.BOTTOM_RIGHT: Element.set_bottom_right}
