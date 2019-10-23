import pygame
from pygame import Rect
from .element import Element
from .element import Anchor
from .text import Text
from .sliced_image import SlicedImage
from util import make_vector
from .drawing import smart_draw
import config


class Button(Element):
    def __init__(self, position, size, background, font, anchor=Anchor.TOP_LEFT, text=None, on_click_callback=None,
                 text_color=config.default_text_color):
        if size is None or (size[0] == 0 and size[1] == 0):
            assert isinstance(background, pygame.Surface) or isinstance(background, SlicedImage)

            size = background.get_rect().size

        super().__init__(position, Rect(*position, *size), anchor)
        self._background = background
        self._text = None

        # text_style = ElementStyle(
        #     background=None,
        #     anchor=Anchor.CENTER,
        #     text_color=text_color,
        #     font=font
        # )
        if text is not None:
            self._text = Text(make_vector(size[0] // 2, size[1] // 2), "", font, text_color)

            self.add_child(self._text)
            self._text.layout()

        self.on_click = on_click_callback
        self._click_down = False

    def draw(self, screen):
        smart_draw(screen, self._background, self.rect)

        super().draw(screen)

    def handle_event(self, evt, game_events):
        super().handle_event(evt, game_events)

        if not evt.consumed:
            if evt.type == pygame.MOUSEBUTTONDOWN:
                self._click_down = self.rect.collidepoint(evt.pos)

                if self._click_down:
                    self.consume(evt)
                    self.make_active()

            elif evt.type == pygame.MOUSEBUTTONUP:
                inside = self.rect.collidepoint(evt.pos)

                if inside and self._click_down:
                    self.clicked()

                    if self.on_click:
                        self.on_click()
                        self.consume(evt)

                self._click_down = False

    def clicked(self):
        pass
