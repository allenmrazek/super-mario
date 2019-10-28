import pygame
from entities.gui import *
import config

default_font = None


def get_default_font():
    global default_font

    default_font = default_font or pygame.font.SysFont(None, 16)

    return default_font


def create_button(gui_atlas, position, size, text=None, on_click_callback=None, font=None, anchor=None, text_color=config.default_text_color):
    bkg = gui_atlas.load_sliced("button_bkg_dark")
    bkg_mo = gui_atlas.load_sliced("button_bkg_light")

    font = font or get_default_font()
    anchor = anchor or Anchor.TOP_LEFT
    text = text or ""

    return Button(position, size, bkg, font, anchor, text, on_click_callback, text_color, bkg_mo)


def create_dialog(gui_atlas, position, size, title, font=None, text_color=config.default_text_color, tb_bkg=None):
    bkg_window = gui_atlas.load_sliced("window_bkg_large")
    font = font or get_default_font()
    tb_bkg = tb_bkg or gui_atlas.load_sliced("tb_frame")

    return Dialog(position, size, bkg_window, font, text_color, tb_bkg, title, additional_height=8, text_start_offset=(12,5))
