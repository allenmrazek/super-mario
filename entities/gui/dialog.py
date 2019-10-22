import pygame
from .element import Element
from .element import Anchor
from .window import Window
from util import make_vector
import config


class _TitleBar(Element):
    def __init__(self, bar_color, text_color, font, text):
        super().__init__(make_vector(0, 0), anchor=Anchor.TOP_LEFT)
        self.surface = font.render(text, True, text_color)
        self.bar_color = bar_color
        self.text_color = text_color
        self.font = font
        self.height = self.surface.get_height()

        self.layout()

    def draw(self, screen):
        # draw title bar
        r = self.get_absolute_rect()
        current_clip = screen.get_clip()
        screen.set_clip(r)

        screen.fill(self.bar_color, r)
        screen.blit(self.surface, r)

        screen.set_clip(current_clip)

    def update(self, dt):
        pass

    def handle_event(self, evt, game_events):
        pass  # todo

    def layout(self):
        self.width = self.parent.width if self.parent is not None else self.width

        # todo: relative position of buttons?
        super().layout()

class Dialog(Window):
    def __init__(self,
                 dialog_position,
                 dialog_size,
                 background,
                 font,
                 text_color=config.default_text_color,
                 tb_color=config.default_window_toolbar_color,
                 title=""):
        super().__init__(dialog_position, dialog_size, background)

        self.text_color = text_color
        self.tb_color = tb_color
        self.title_bar = _TitleBar(tb_color, text_color, font, title)
        self.add_child(self.title_bar)
