from abc import abstractmethod, ABC
import random
import copy
import pygame
from state.game_state import GameState, state_stack
from state.test_level import TestLevel
from entities.gui import Frame, Element, Anchor, Scrollbar, ScrollbarType
from editor.dialogs import ToolDialog, LayerDialog, TilePickerDialog, ModeDialog, LevelConfigDialog
from entities.entity import EntityManager, Layer
from assets.asset_manager import AssetManager
import config
from util import make_vector, bind_callback_parameters
from assets import Level
from event import EventHandler
from util import pixel_coords_to_tile_coords
from .place_mode import PlaceMode
from .passable_mode import PassableMode
from .config_mode import ConfigMode


class _ModeDrawHelper(Element):
    """Exists only as a way to get a callback just before the first UI elements are drawn"""
    def __init__(self, draw_callback):
        super().__init__(make_vector(0, 0), None, Anchor.TOP_LEFT)

        self.draw_callback = draw_callback

    def draw(self, screen, view_rect):
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

        # scrollbars to move map
        self.scroll_map_horizontal = Scrollbar(pygame.Vector2(*config.screen_rect.bottomleft) + make_vector(10, -20),
                                               ScrollbarType.HORIZONTAL, config.screen_rect.width - 20,
                                               self.assets.gui_atlas.load_sliced("option_button"),
                                               self.assets.gui_atlas.load_sliced("sb_thumb_h"),
                                               self.level.tile_map.width * self.level.tile_map.tileset.tile_width,
                                               sb_button_mouseover=self.assets.gui_atlas.load_sliced("sb_thumb_h_hl"),
                                               on_value_changed_callback=bind_callback_parameters(self.on_horizontal_scroll))

        self.scroll_map_vertical = Scrollbar(pygame.Vector2(*config.screen_rect.topright) + make_vector(-20, 10),
                                             ScrollbarType.VERTICAL, config.screen_rect.height - 40,
                                               self.assets.gui_atlas.load_sliced("option_button"),
                                               self.assets.gui_atlas.load_sliced("sb_thumb_v"),
                                               self.level.tile_map.height * self.level.tile_map.tileset.tile_height,
                                               sb_button_mouseover=self.assets.gui_atlas.load_sliced("sb_thumb_v_hl"),
                                               on_value_changed_callback=bind_callback_parameters(self.on_vertical_scroll))

        self.frame.add_child(self.scroll_map_horizontal)
        self.frame.add_child(self.scroll_map_vertical)

        # ... the various dialogs used by editor
        self.tool_dialog = ToolDialog(self.assets.gui_atlas)
        self.frame.add_child(self.tool_dialog)

        self.layer_dialog = LayerDialog(self.assets.gui_atlas)
        self.frame.add_child(self.layer_dialog)

        self.tile_dialog = TilePickerDialog(self.assets)
        self.frame.add_child(self.tile_dialog)

        self.config_dialog = LevelConfigDialog(self.level, self.assets.gui_atlas)
        self.frame.add_child(self.config_dialog)

        # editor states to handle relevant actions
        self.current_mode = None

        self.place_mode = PlaceMode(self.tile_dialog, self.level)
        self.passable_mode = PassableMode(self.level)
        self.config_mode = ConfigMode()

        self.set_mode(self.place_mode)

        self.mode_dialog = ModeDialog(self.assets.gui_atlas,
                                      on_tile_mode_callback=bind_callback_parameters(self.set_mode, self.place_mode),
                                      on_passable_mode_callback=
                                      bind_callback_parameters(self.set_mode, self.passable_mode),
                                      on_config_mode_callback=bind_callback_parameters(self.set_mode, self.config_mode))

        self.frame.add_child(self.mode_dialog)

    def draw(self, screen):
        screen.fill(self.level.background_color)
        self.level.draw(screen)
        self.entity_manager.draw(screen, self.level.view_rect)

    def set_mode(self, new_mode):
        if new_mode is self.place_mode:
            # turn on/off relevant dialogs
            self.tile_dialog.enabled = True
            self.tool_dialog.enabled = True
            self.layer_dialog.enabled = True
            self.config_dialog.enabled = False

        elif new_mode is self.passable_mode:
            self.tile_dialog.enabled = False
            self.tool_dialog.enabled = False
            self.layer_dialog.enabled = False
            self.config_dialog.enabled = False
        elif new_mode is self.config_mode:
            self.tile_dialog.enabled = False
            self.tool_dialog.enabled = False
            self.layer_dialog.enabled = False
            self.config_dialog.enabled = True
        else:
            raise NotImplementedError  # unknown mode

        self.current_mode = new_mode

    def update(self, dt):
        self.entity_manager.update(dt, self.level.view_rect)

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

    def on_horizontal_scroll(self, new_val):
        existing = self.level.position
        existing.x = new_val
        self.level.position = existing

    def on_vertical_scroll(self, new_val):
        existing = self.level.position
        existing.y = new_val
        self.level.position = existing
