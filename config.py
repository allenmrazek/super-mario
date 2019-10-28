from pygame import Rect
from pygame import Color

debug_jumps = True
debug_hitboxes = True

screen_size = 1024, 675
screen_rect = Rect(0, 0, *screen_size)

base_tile_dimensions = (16, 16)  # tiles on disk are treated as this dimension
rescale_factor = 2  # all loaded sprites and images will be rescaled by this value

transparent_color = Color('magenta')

PHYSICS_DT = 1. / 60

default_background_color = Color('black')
default_text_color = Color('white')
default_window_toolbar_color = Color('blue')
default_window_background = Color('red')

editor_grid_color = (255, 0, 0, 128)
editor_grid_overlay_color = (255, 0, 0, 255)
