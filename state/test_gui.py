from pygame import Rect
from .game_state import GameState
from entities.gui import Window
from entities.gui.element import Anchor
from entities.gui import Text
from util import make_vector
import config


class TestGui(GameState):
    def __init__(self, game_events):
        super().__init__(game_events)

        self.window = Window(make_vector(0, 0), Rect(0, 0, 256, 256), (0, 255, 0), anchor=Anchor.TOP_LEFT)

        text = Text(make_vector(self.window.rect.width, 0), anchor=Anchor.TOP_RIGHT)
        text.text = "Hello, world!"
        self.window.add(text)

    def update(self, dt):
        self.window.update(dt)

    def draw(self, screen):
        self.window.draw(screen)

        clr = (255, 0, 0)
        r = Rect(config.screen_rect.width - 256, 0, 256, 256)
        screen.fill(clr, r)

    @property
    def finished(self):
        return False