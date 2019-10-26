from abc import abstractmethod, ABC
import random
import copy
import pygame
from state.game_state import GameState, state_stack
from state.test_level import TestLevel
from entities.gui import Frame, Element, Anchor
from editor.dialogs import ToolDialog, LayerDialog, TilePickerDialog
from entities.entity import EntityManager, Layer
from assets.asset_manager import AssetManager
import config
from util import make_vector
from level import Level
from event import EventHandler
from util import pixel_coords_to_tile_coords
from .place_mode import PlaceMode
from .passable_mode import PassableMode


class _ModeDrawHelper(Element):
    """Exists only as a way to get a callback just before the first UI elements are drawn"""
    def __init__(self, draw_callback):
        super().__init__(make_vector(0, 0), None, Anchor.TOP_LEFT)

        self.draw_callback = draw_callback

    def draw(self, screen):
        self.draw_callback(screen)


class EditorState(GameState, EventHandler):
    def __init__(self, game_events, assets):
        super().__init__(game_events)

        self.assets = assets  # type: AssetManager
        self.entity_manager = EntityManager([Layer.Interface])

        # create a level to edit
        self.level = Level(assets)

        # shim to create a callback before UI draws
        self.entity_manager.register(_ModeDrawHelper(self.on_pre_ui_draw))

        # frame to contain all other windows
        self.frame = Frame(make_vector(0, 0), config.screen_rect.size)
        self.entity_manager.register(self.frame)

        self.tool_dialog = EditorState.create_tool_dialog(self.assets.gui_atlas)
        self.frame.add_child(self.tool_dialog)

        self.layer_dialog = EditorState.create_layer_dialog(self.assets.gui_atlas)
        self.frame.add_child(self.layer_dialog)

        self.tile_dialog = EditorState.create_tile_dialog(self.assets)
        self.frame.add_child(self.tile_dialog)

        # editor states to handle relevant actions

        self.current_mode = None

        self.place_mode = PlaceMode(self.tile_dialog, self.level.map)
        self.passable_mode = PassableMode(self.level.map)
        self.set_mode(self.passable_mode)

    def draw(self, screen):
        screen.fill(config.default_background_color)
        self.level.draw(screen)
        self.entity_manager.draw(screen)

    def set_mode(self, new_mode):
        if new_mode is self.place_mode:
            # turn on/off relevant dialogs
            pass
        elif new_mode is self.passable_mode:
            self.tile_dialog.enabled = False
            self.tool_dialog.enabled = False
            self.layer_dialog.enabled = False

            self.current_mode = new_mode

    def update(self, dt):
        self.entity_manager.update(dt)

    @property
    def finished(self):
        return False

    def on_pre_ui_draw(self, screen):
        self.current_mode.draw(screen)

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
                self.consume(evt)
                self.current_mode.on_map_click(evt, pygame.mouse.get_pos())

            elif evt.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                self.consume(evt)
                self.current_mode.on_map_mousedown(evt, pygame.mouse.get_pos())

            elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_t:
                # copy level state -> we don't want the actual movement and deaths of entities to be reflected
                # in our copy of the level
                print("warning: shallow copy of level")

                # easiest way to handle this is to serialize our level, then load it rather than some
                # complicated deepcopy incomplementation
                state_stack.push(TestLevel(self.game_events, self.assets, self.level))

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
