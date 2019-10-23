import pygame
from entities.gui.element import Element, ElementStyle
from .element import Anchor
from .drawing import smart_draw
import config


class Text(Element):
    def __init__(self, element_position, text, style: ElementStyle):
        # color=config.default_text_color, anchor=Anchor.CENTER,
        #          anti_alias=True, bg_color=None):
        super().__init__(element_position, anchor=style.anchor)

        # todo: actual SMB font
        self.font = style.font
        self._next_text = text
        self._text = ""
        self.color = style.text_color
        self.anti_alias = style.anti_alias
        self.background = style.background
        self.surface = None
        self._create_text_surface()

    def handle_event(self, evt, game_events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        if self._next_text != self._text:
            # only create text surfaces when old ones are in need of updating
            self._create_text_surface()
            self._text = self._next_text

        screen.blit(self.surface, self.rect)

    @property
    def text(self):
        return self._next_text

    @text.setter
    def text(self, new_text):
        self._next_text = new_text

    def _create_text_surface(self):
        self._text = self._next_text

        if self.background is None or isinstance(self.background, pygame.Color) or isinstance(self.background, tuple):
            # simple color background
            self.surface = self.font.render(self._next_text, self.anti_alias, self.color, self.background)
        else:
            # have some complex background that must be blitted first
            surf_dimensions = self.font.size(self._next_text)

            self.surface = pygame.Surface(surf_dimensions).convert_alpha()  # want 32 bit
            self.surface.fill(config.transparent_color)

            smart_draw(self.surface, self.background, self.background.get_rect())

            # render text into another temp surface
            text_surface = self.font.render(self._next_text, self.anti_alias, self.color, None)

            # blit this text onto background surface
            self.surface.blit(text_surface, text_surface.get_rect())

        self.width, self.height = self.surface.get_width(), self.surface.get_height()

        # update surface position based on anchor
        self.layout()
