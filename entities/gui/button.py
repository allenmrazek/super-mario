from copy import copy
import pygame
from pygame import Rect
from .element import Element
from .element import Anchor
from .text import Text
from util import make_vector
import config


class Button(Element):
    def __init__(self, position, sliced_image, text=None, on_click=None, size=None,
                 anchor=Anchor.TOP_LEFT, text_color=config.default_text_color):
        if size is None:
            size = self._sliced_image.get_rect().size

        super().__init__(position, Rect(*position, *size), anchor)
        self._sliced_image = sliced_image
        self._text = None

        if text is not None:
            self._text = Text(make_vector(size[0] // 2, size[1] // 2),
                              anchor=Anchor.CENTER, color=text_color, text=text)
            self.add_child(self._text)
            self._text.layout()

        self.on_click = on_click
        self._click_down = False

    def draw(self, screen):
        self._sliced_image.draw(screen, self.rect)
        super().draw(screen)

    def handle_event(self, evt, game_events):
        super().handle_event(evt, game_events)

        if not evt.consumed:
            if evt.type == pygame.MOUSEBUTTONDOWN:
                self._click_down = self.rect.collidepoint(evt.pos)

                if self._click_down:
                    self.consume(evt)

            elif evt.type == pygame.MOUSEBUTTONUP:
                inside = self.rect.collidepoint(evt.pos)

                if inside and self._click_down:
                    if self.on_click:
                        self.on_click()
                        self.consume(evt)

                self._click_down = False
