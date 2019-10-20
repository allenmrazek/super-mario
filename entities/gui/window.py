from .element import Element
from .element import Anchor
from event.game_events import EventHandler
import pygame
from util import copy_vector


class Window(Element, EventHandler):
    def __init__(self, window_position, rect, background, anchor=Anchor.CENTER):
        super().__init__(window_position, anchor, rect)

        assert background is not None
        assert isinstance(background, pygame.Surface) or isinstance(background, pygame.Color) \
            or isinstance(background, tuple)

        self.element_position = copy_vector(window_position)
        self.background = background
        self.update_element_position()
        self._window_elements = []

    def draw(self, screen: pygame.Surface):
        r = screen.get_rect().clip(self.rect)

        if isinstance(self.background, pygame.Surface):
            screen.blit(self.background, r)
        else:
            screen.fill(self.background, r)

        screen.set_clip(r)

        for element in self._window_elements:
            element.draw(screen)

        screen.set_clip(None)

    def update(self, dt):
        for element in self._window_elements:
            element.update(dt)

    def handle_event(self, evt, game_events):
        # todo: own events?

        for element in self._window_elements:
            element.handle_event(evt)

            if evt.consumed:
                break

    def add(self, ui_element):
        if ui_element not in self._window_elements:
            self._window_elements.append(ui_element)

            # assume element's position is relative to our own
            ui_element.element_position = self.element_position + ui_element.element_position

    def remove(self, ui_element):
        self._window_elements.remove(ui_element)

        # relative->local coordinates
        ui_element.element_position = self.element_position - ui_element.element_position

    # todo: move child elements when position changed
