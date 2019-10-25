import random
import pygame
from .game_state import GameState
from entities.gui import Frame
from editor.dialogs import ToolDialog, LayerDialog, TilePickerDialog
from entities.entity import EntityManager, Layer
from assets.asset_manager import AssetManager
import config
from util import make_vector
from level import Level
from event import EventHandler


class EditorState(GameState, EventHandler):
    def __init__(self, game_events, assets):
        super().__init__(game_events)

        self.assets = assets  # type: AssetManager

        # create a level to edit
        self.level = Level(assets)

        # frame to contain all other windows
        self.frame = Frame(make_vector(0, 0), config.screen_rect.size)

        self.entity_manager = EntityManager({Layer.Interface: set()}, [Layer.Interface])
        self.entity_manager.register(self.frame)

        self.tool_dialog = EditorState.create_tool_dialog(self.assets.gui_atlas)
        self.frame.add_child(self.tool_dialog)

        self.layer_dialog = EditorState.create_layer_dialog(self.assets.gui_atlas)
        self.frame.add_child(self.layer_dialog)

        self.tile_dialog = EditorState.create_tile_dialog(self.assets)
        self.frame.add_child(self.tile_dialog)

    def draw(self, screen):
        screen.fill(config.default_background_color)
        self.level.draw(screen)
        self.entity_manager.draw(screen)

    def update(self, dt):
        self.entity_manager.update(dt)

    @property
    def finished(self):
        return False

    def activated(self):
        self.game_events.register(self)

    def deactivated(self):
        self.game_events.unregister(self)

    def handle_event(self, evt, game_events):
        self.frame.handle_event(evt, game_events)

        # if absolutely nothing handled the event, the user has tried to do some kind of interaction
        # with the map itself
        if not self.is_consumed(evt):
            if evt.type == pygame.MOUSEBUTTONDOWN:
                print("clicked on map")

                # as a super rough test thing, let's try and change a tile with this
                x = random.randint(0, self.level.map.width - 1)
                y = random.randint(0, self.level.map.height - 1)
                idx = random.randint(0, self.level.asset_manager.tileset.tile_count - 1)

                self.level.map.set_tile((x, y), idx)

    @staticmethod
    def create_tool_dialog(atlas):
        dialog = ToolDialog(atlas)

        # todo: set up callbacks?

        return dialog

    @staticmethod
    def create_layer_dialog(atlas):
        dialog = LayerDialog(atlas)

        # todo

        return dialog

    @staticmethod
    def create_tile_dialog(asset_manager):
        dialog = TilePickerDialog(asset_manager)

        # todo

        return dialog
