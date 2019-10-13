from pygame import Rect
from pygame import Color

screen_size = 256, 240
screen_rect = Rect(0, 0, *screen_size)

transparent_color = Color('magenta')

PHYSICS_DT = 1. / 60
