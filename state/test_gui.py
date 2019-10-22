import pygame
from pygame import Rect
from .game_state import GameState
from entities.gui import Window, WindowParameters
from entities.gui.element import Anchor
from entities.gui import Text
from entities.gui import Button
from entities.gui import Texture
from util import make_vector
from entities.gui import SlicedImage
import config


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

        # text inside the window
        text = Text(make_vector(128, 128), anchor=Anchor.TOP_LEFT)
        text.text = "Hello, world!"
        self.window.add_child(text)

        # add a button to the window
        def test_click():
            print("clicked!")

        # add an image to the window
        texture = Texture("images/atlas.png", make_vector(0, 256), anchor=Anchor.BOTTOM_LEFT)
        self.window.add_child(texture)

        button = Button(make_vector(0, 0), SlicedImage(), size=(128, 48), text="click me",
                        on_click=test_click, text_color=pygame.Color('black'))

        self.window.add_child(button)

        game_events.register(self.window)

    def update(self, dt):
        self.window.update(dt)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.window.draw(screen)

        clr = (255, 0, 0)
        r = Rect(config.screen_rect.width - 256, 0, 256, 256)
        screen.fill(clr, r)

    @property
    def finished(self):
        return False
