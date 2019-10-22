import pygame
from entities.gui import Text, Texture, Window, WindowParameters
import config


class ToolDialog(Window):
    SIZE = (256, 128)

    def __init__(self):
        params = WindowParameters(bar_color=config.default_window_toolbar_color, text_color=config.default_text_color,
                                  height=0, title="Tools", font=pygame.font.SysFont("", 16))

        super().__init__((0, 0), rect=pygame.Rect(0, 0, *ToolDialog.SIZE), background=config.default_window_background)
