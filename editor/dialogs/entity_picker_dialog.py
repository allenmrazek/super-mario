import warnings
import pygame
from entities.gui import Dialog, ScrollbarType, Scrollbar, Button, Container
from util import make_vector
from entities.characters.level_entity import LevelEntity
from util import bind_callback_parameters
from assets.level import Level


class PickedEntity:
    def __init__(self, entity_name, level):
        assert entity_name in LevelEntity.Factories.keys()

        self.name = entity_name
        factory = LevelEntity.Factories[entity_name]

        # create a fake level, since we don't want any factory to affect the real level
        fake_level = Level(level.asset_manager)

        # create preview image
        preview_entity = factory(fake_level, None)

        self.preview_surface = preview_entity.create_preview()

    @staticmethod
    def _get_current_entities(entity_manager):
        existing_entities = {}

        for layer, contents in entity_manager.layers.items():
            existing_entities[layer.name] = set([x for x in contents])

        return existing_entities


class EntityPickerDialog(Dialog):
    SIZE = (256, 256)
    BUTTON_SIZE = (200, 20)

    def __init__(self, level):
        font = pygame.font.SysFont(None, 24)

        self.level = level
        self.assets = level.asset_manager

        super().__init__(make_vector(0, 0),
                         EntityPickerDialog.SIZE, self.assets.gui_atlas.load_sliced("bkg_rounded"),
                         font=font, title="Tiles")

        # create contents (buttons for each entity)
        self.scrolling_container = self._create_container(font)

        # create vertical scrollbar
        self.vertical_scroll = Scrollbar(make_vector(self.scrolling_container.rect.right, self.scrolling_container.rect.top + 5),
                                         ScrollbarType.VERTICAL, self.scrolling_container.rect.height,
                                         self.assets.gui_atlas.load_sliced("control_small_block2"),
                                         self.assets.gui_atlas.load_sliced("sb_thumb_v"),
                                         max(0, self.scrolling_container.height),
                                         sb_button_mouseover=self.assets.gui_atlas.load_sliced("sb_thumb_v_hl"),
                                         on_value_changed_callback=self._on_scroll_changed)

        self.add_child(self.scrolling_container)
        self.add_child(self.vertical_scroll)

        self.layout()

        self.selected_entity = None

    def _on_scroll_changed(self, new_val):
        self.scrolling_container.offset = make_vector(0, self.vertical_scroll.value)
        self.scrolling_container.layout()

    def _make_selection(self, entity_name):
        self.selected_entity = PickedEntity(entity_name, self.level)

    def _create_container(self, font):
        y_offset = 0

        frame = Container(make_vector(10, self.get_title_bar_bottom() + 4),
                      (EntityPickerDialog.SIZE[0] - 20,
                       EntityPickerDialog.SIZE[0] - self.get_title_bar_bottom() - 8))

        for name, factory in LevelEntity.Factories.items():
            entity_button = Button(make_vector(10, y_offset),
                                   size=EntityPickerDialog.BUTTON_SIZE,
                                   background=self.assets.gui_atlas.load_sliced("option_button"),
                                   font=font,
                                   text=name,
                                   on_click_callback=bind_callback_parameters(self._make_selection, name),
                                   text_color=(0, 0, 0),
                                   mouseover_image=self.assets.gui_atlas.load_sliced("option_button_hl"))

            frame.add_child(entity_button)
            y_offset += entity_button.height + 3

        return frame
