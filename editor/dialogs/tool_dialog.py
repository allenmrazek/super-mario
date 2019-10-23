import pygame
from entities.gui import Text, Texture, Window, Dialog
import config
from util import make_vector


class ToolDialog(Dialog):
    SIZE = (256, 128)

    def __init__(self, atlas):
        font=pygame.font.SysFont("", 24)

        r = config.screen_rect.copy()
        super().__init__(make_vector(r.right - ToolDialog.SIZE[0], r.top),
                         ToolDialog.SIZE, atlas.load_sliced("rounded_corners"),
                         font=font, title="Tools")

        # todo: tool types
