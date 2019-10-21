import pygame
from entities.gui.element import Element
from .element import Anchor


class Text(Element):
    def __init__(self, element_position, text="", color=pygame.Color('white'), anchor=Anchor.CENTER,
                 anti_alias=True, bg_color=None):
        super().__init__(element_position, anchor=anchor)

        # todo: actual SMB font
        self.font = pygame.sysfont.SysFont(None, 24, color)
        self._next_text = text
        self._text = ""
        self.color = color
        self.anti_alias = anti_alias
        self.bg_color = bg_color
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

        self.surface = self.font.render(self._next_text, self.anti_alias, self.color, self.bg_color)
        self.width, self.height = self.surface.get_width(), self.surface.get_height()

        # update surface position based on anchor
        self.layout()
