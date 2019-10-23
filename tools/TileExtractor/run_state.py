import pygame
from entities.gui import Dialog, Button
from state import GameState
from event import EventHandler
from entities import EntityManager, Layer
import config
from util import make_vector


class RunState(GameState, EventHandler):
    def __init__(self, game_events, atlas):
        super().__init__(game_events)
        self._quit = False

        font = pygame.font.SysFont(None, 16)

        self.entities = EntityManager({Layer.Interface: set()}, [Layer.Interface])

        button_size = 128, 34

        # create classifier dialog
        self.classifier_dialog = Dialog(
            make_vector(config.screen_rect.centerx, config.screen_rect.bottom - 128),
            (128, 256),
            background=atlas.load_sliced("bkg_square"),
            font=font,
            text_color=pygame.Color('white'),
            tb_color=pygame.Color('blue'),
            title="Classify Tiles"
        )

        # create 'background' button
        background_button = Button(
            make_vector(0, 0),
            size=button_size,
            background=atlas.load_sliced("bkg_square"),
            font=font,
            text="Background",
            text_color=pygame.Color('black'),
            mouseover_image=atlas.load_sliced("bkg_square_hl")
        )

        # create 'solid block / not interactive' button
        solid_noninteractive = Button(
            make_vector(0, 0),
            size=button_size,
            background=atlas.load_sliced("bkg_square"),
            font=font,
            text="Solid + Not Interactive",
            text_color=pygame.Color('black'),
            mouseover_image=atlas.load_sliced("bkg_square_hl")
        )

        # create 'solid block / interactive' button
        solid_interactive = Button(
            make_vector(0, 0),
            size=button_size,
            background=atlas.load_sliced("bkg_square"),
            font=font,
            text="Solid + Interactive",
            text_color=pygame.Color('black'),
            mouseover_image=atlas.load_sliced("bkg_square_hl")
        )

        # create 'skip' button
        skip = Button(
            make_vector(0, 0),
            size=button_size,
            background=atlas.load_sliced("bkg_square"),
            font=font,
            text="Skip",
            text_color=pygame.Color('black'),
            mouseover_image=atlas.load_sliced("bkg_square_hl")
        )

        buttons = [background_button, solid_noninteractive, solid_interactive, skip]

        y_pos = self.classifier_dialog.get_title_bar_bottom()

        for btn in buttons:
            btn.relative_position = make_vector(0, y_pos)
            y_pos += btn.height

            self.classifier_dialog.add_child(btn)

        self.classifier_dialog.add_child(background_button)

        self.classifier_dialog.height = y_pos
        self.classifier_dialog.position = config.screen_rect.center

        self.classifier_dialog.layout()

        self.entities.register(self.classifier_dialog)
        game_events.register(self.classifier_dialog)

    def update(self, dt):
        self.entities.update(dt)

    def draw(self, screen):
        screen.fill(config.transparent_color)
        self.entities.draw(screen)

    @property
    def finished(self):
        return self._quit

    def handle_event(self, evt, game_events):
        if evt.type == pygame.QUIT or (evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE):
            self._quit = True
