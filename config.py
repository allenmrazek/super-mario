from pygame import Rect
from pygame import Color

debug_jumps = True

screen_size = 1024, 675
screen_rect = Rect(0, 0, *screen_size)

rescale_factor = 4  # all loaded sprites and images will be rescaled by this value

transparent_color = Color('magenta')

PHYSICS_DT = 1. / 60
