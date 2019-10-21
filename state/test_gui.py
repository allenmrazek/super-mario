import pygame
from pygame import Rect
from .game_state import GameState
from entities.gui import Window, WindowParameters
from entities.gui.element import Anchor
from entities.gui import Text
from util import make_vector
import config

from entities.gui import SlicedImage

class TestGui(GameState):
    def __init__(self, game_events):
        super().__init__(game_events)

        font = pygame.font.SysFont("", 16)

        self.window = Window(make_vector(0, 0), Rect(0, 0, 256, 256), (0, 255, 0),
                             anchor=Anchor.TOP_LEFT,
                             params=WindowParameters(
                                 bar_color=pygame.Color('red'),
                                 text_color=pygame.Color('blue'),
                                 font=font, title="Hello!", height=0))

        text = Text(make_vector(128, 128), anchor=Anchor.TOP_LEFT)
        text.text = "Hello, world!"
        self.window.add_child(text)

        game_events.register(self.window)

        self.sliced = SlicedImage((4, 4))

    def update(self, dt):
        self.window.update(dt)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.window.draw(screen)

        clr = (255, 0, 0)
        r = Rect(config.screen_rect.width - 256, 0, 256, 256)
        screen.fill(clr, r)

        self.sliced.draw(screen, pygame.Rect(0, 0, 256, 256))

    @property
    def finished(self):
        return False
