import pygame
from entities.gui import Text, Texture, Window, Dialog, Option, OptionGroup, Scrollbar, ScrollbarType
from entities.entity import Layer
from entities.gui import Anchor
import config
from util import make_vector, clamp


class LevelConfigDialog(Dialog):
    SIZE = 256, 256

    def __init__(self, level, atlas):
        font = pygame.font.SysFont("", 16)

        r = config.screen_rect.copy()
        title = "Level Configuration"

        width, height = LevelConfigDialog.SIZE

        pos = make_vector(*r.center)

        super().__init__(pos, (width, height), atlas.load_sliced("bkg_rounded"),
                         font=font, title=title)

        self.level = level
        black = pygame.Color('black')

        # Background color text
        bkg_color_text = Text(make_vector(10, self.get_title_bar_bottom()), text="Background Color",
                              font=font, text_color=black)

        self.add_child(bkg_color_text)

        # slider for r
        r_text = Text(make_vector(10, bkg_color_text.relative_position.y + bkg_color_text.height),
                      text="R:", font=font, text_color=black)

        self.add_child(r_text)

        self.bkg_color_r_slider = Scrollbar(make_vector(r_text.relative_position.x + 30, bkg_color_text.relative_position.y + bkg_color_text.height),
                                            ScrollbarType.HORIZONTAL, LevelConfigDialog.SIZE[0] - 60,
                                            atlas.load_sliced("control_small_block2"),
                                            atlas.load_sliced("sb_thumb_h"),
                                            255,
                                            0,
                                            atlas.load_sliced("sb_thumb_h_dk"),
                                            self._on_slider_changed)

        # slider for g
        g_text = Text(make_vector(10, self.bkg_color_r_slider.relative_position.y + self.bkg_color_r_slider.height),
                      text="G:", font=font, text_color=black)

        self.add_child(g_text)

        self.bkg_color_g_slider = Scrollbar(make_vector(g_text.relative_position.x + 30, r_text.relative_position.y + g_text.height),
                                            ScrollbarType.HORIZONTAL, LevelConfigDialog.SIZE[0] - 60,
                                            atlas.load_sliced("control_small_block2"),
                                            atlas.load_sliced("sb_thumb_h"),
                                            255,
                                            0,
                                            atlas.load_sliced("sb_thumb_h_dk"),
                                            self._on_slider_changed)

        # slider for b
        b_text = Text(make_vector(10, self.bkg_color_g_slider.relative_position.y + self.bkg_color_g_slider.height),
                      text="B:", font=font, text_color=black)

        self.add_child(b_text)

        self.bkg_color_b_slider = Scrollbar(make_vector(b_text.relative_position.x + 30, g_text.relative_position.y + b_text.height),
                                            ScrollbarType.HORIZONTAL, LevelConfigDialog.SIZE[0] - 60,
                                            atlas.load_sliced("control_small_block2"),
                                            atlas.load_sliced("sb_thumb_h"),
                                            255,
                                            0,
                                            atlas.load_sliced("sb_thumb_h_dk"),
                                            self._on_slider_changed)

        self.add_child(self.bkg_color_r_slider)
        self.add_child(self.bkg_color_g_slider)
        self.add_child(self.bkg_color_b_slider)

    def _on_slider_changed(self, new_value):
        r = clamp(int(self.bkg_color_r_slider.value), 0, 255)
        g = clamp(int(self.bkg_color_g_slider.value), 0, 255)
        b = clamp(int(self.bkg_color_b_slider.value), 0, 255)

        self.level.background_color = pygame.Color((r, g, b))
