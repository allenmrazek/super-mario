from enum import Enum
import pygame
from .entity import Entity
from .entity import Layer
from util import copy_vector


class TextAnchor(Enum):
    CENTER = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4


class Text(Entity):
    _text_position_setters = {}

    def __init__(self, text_position, text="", color=pygame.Color('white'), anchor=TextAnchor.CENTER, anti_alias=True, bg_color=None):
        super().__init__(pygame.Rect(0, 0, 0, 0))

        # todo: actual SMB font
        self.font = pygame.sysfont.SysFont(None, 24, color)
        self._next_text = text
        self._text = ""
        self.color = color
        self.anchor = anchor
        self.anti_alias = anti_alias
        self.bg_color = bg_color
        self.text_position = copy_vector(text_position)
        self.surface = None
        self._create_text_surface()

    def update(self, dt):
        pass

    def draw(self, screen):
        if self._next_text != self._text:
            # only create text surfaces when old ones are in need of updating
            self._create_text_surface()
            self._text = self._next_text

        screen.blit(self.surface, self.rect)

    @property
    def layer(self):
        return Layer.Overlay

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
        Text._text_position_setters[self.anchor](self)

    @staticmethod
    def set_center(text_entity):
        text_entity.x = text_entity.text_position.x - text_entity.width // 2
        text_entity.y = text_entity.text_position.y - text_entity.height // 2

    @staticmethod
    def set_top_left(text_entity):
        text_entity.x, text_entity.y = text_entity.text_position

    @staticmethod
    def set_top_right(text_entity):
        tp = text_entity.text_position

        text_entity.x, text_entity.y = tp.x - text_entity.width, tp.y

    @staticmethod
    def set_bottom_left(text_entity):
        tp = text_entity.text_position

        text_entity.x, text_entity.y = tp.x, tp.y - text_entity.height

    @staticmethod
    def set_bottom_right(text_entity):
        tp = text_entity.text_position

        text_entity.x = tp.x - text_entity.width
        text_entity.y = tp.y - text_entity.height


Text._text_position_setters = {TextAnchor.CENTER: Text.set_center,
                                 TextAnchor.TOP_LEFT: Text.set_top_left,
                                 TextAnchor.TOP_RIGHT: Text.set_top_right,
                                 TextAnchor.BOTTOM_LEFT: Text.set_bottom_left,
                                 TextAnchor.BOTTOM_RIGHT: Text.set_bottom_right}
