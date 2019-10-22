import pygame
from pygame import Rect
from .game_state import GameState
from entities.entity import EntityManager, Layer
from entities.gui import Window, Text, Button, Texture, Dialog, SlicedImage
from entities.gui import Anchor
from entities.gui import Frame
from util import make_vector
import config


class TestGui(GameState):
    def __init__(self, game_events):
        super().__init__(game_events)

        font = pygame.font.SysFont("", 16)

        # self.window = Window(make_vector(0, 0), Rect(0, 0, 256, 256), (0, 255, 0),
        #                      anchor=Anchor.TOP_LEFT,
        #                      params=WindowParameters(
        #                          bar_color=pygame.Color('red'),
        #                          text_color=pygame.Color('blue'),
        #                          font=font, title="Hello!", height=0))
        self.window = Window(make_vector(0, 0), (256, 256), (0, 255, 0))

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

        # add a button to the window
        button = Button(make_vector(0, 0), SlicedImage(), size=(128, 48), text="click me",
                        on_click=test_click, text_color=pygame.Color('black'))

        self.window.add_child(button)

        # create a dialog window
        self.dialog = Dialog(make_vector(512, 0), (200, 200), (128, 128, 128),
                             title="Dialog Title Here",
                             font=pygame.sysfont.SysFont(None, 16, config.default_text_color))

        # create a frame which will deal with ordering the windows
        self.frame = Frame(make_vector(0, 0), config.screen_size)
        self.game_events.register(self.frame)

        # add windows to the frame
        self.frame.add_child(self.window)
        self.frame.add_child(self.dialog)

    def update(self, dt):
        self.frame.update(dt)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.frame.draw(screen)

        clr = (255, 0, 0)
        r = Rect(config.screen_rect.width - 256, 0, 256, 256)
        screen.fill(clr, r)

    @property
    def finished(self):
        return False
