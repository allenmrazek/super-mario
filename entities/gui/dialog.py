import pygame
from .element import Element
from .element import Anchor
from .window import Window
from util import make_vector
import config
from entities.gui.drawing import smart_draw


class _TitleBar(Element):
    def __init__(self, bkg, text_color, font, text, tb_extra_height=None, tb_text_offset=None):
        super().__init__(make_vector(0, 0), anchor=Anchor.TOP_LEFT)
        self.surface = font.render(text, True, text_color)
        self.bkg = bkg
        self.text_color = text_color
        self.font = font
        self.height = self.surface.get_height() + (tb_extra_height or 0)
        self.text_offset = tb_text_offset or (0, 0)

        self.layout()

    def draw(self, screen, view_rect):
        # draw title bar
        r = screen.get_rect().clip(self.get_absolute_rect())

        current_clip = screen.get_clip()
        screen.set_clip(r)

        #screen.fill(self.bar_color, r)
        smart_draw(screen, self.bkg, r)

        screen.blit(self.surface, (r.x + self.text_offset[0], r.y + self.text_offset[1]))

        screen.set_clip(current_clip)

    def update(self, dt, view_rect):
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
                 background_window,
                 font,
                 text_color=config.default_text_color,
                 tb_bkg=config.default_window_toolbar_color,
                 title="",
                 additional_height=4, text_start_offset=(6, 2)):
        super().__init__(dialog_position, dialog_size, background_window, Anchor.TOP_LEFT)
        # todo: allow anchor for dialogs?

        self.text_color = text_color
        self.title_bar = _TitleBar(tb_bkg, text_color, font, title,
                                   tb_extra_height=additional_height, tb_text_offset=text_start_offset)
        self.add_child(self.title_bar)

    def get_title_bar_bottom(self):
        return self.title_bar.height
