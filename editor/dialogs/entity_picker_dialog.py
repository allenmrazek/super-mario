import pygame
from entities.gui import Dialog, ScrollableContents, ScrollbarType, Scrollbar, Button, Container
import config
from util import make_vector
from util import tile_coords_to_pixel_coords
from util import pixel_coords_to_tile_coords
from util import tile_index_to_coords
from entities.characters.level_entity import LevelEntity
from util import bind_callback_parameters


class EntityPickerDialog(Dialog):
    SIZE = (256, 256)
    BUTTON_SIZE = (200, 20)

    def __init__(self, assets):
        font = pygame.font.SysFont(None, 24)
        self.assets = assets

        super().__init__(make_vector(0, 0),
                         EntityPickerDialog.SIZE, assets.gui_atlas.load_sliced("bkg_rounded"),
                         font=font, title="Tiles")

        # create contents (buttons for each entity)
        # self.scrolling_container = self._create_container(font)
        #
        # # contents window
        # self.scrollable = ScrollableContents(
        #     make_vector(6, self.get_title_bar_bottom()),
        #     (EntityPickerDialog.SIZE[0] - 25, EntityPickerDialog.SIZE[1] - self.get_title_bar_bottom() - 22),
        #     self.scrolling_container
        # )
        self.scrolling_container = self._create_container(font)

        # create vertical scrollbar

        self.vertical_scroll = Scrollbar(make_vector(self.scrolling_container.rect.right, self.scrolling_container.rect.top + 5),
                                         ScrollbarType.VERTICAL, self.scrolling_container.rect.height,
                                         assets.gui_atlas.load_sliced("control_small_block2"),
                                         assets.gui_atlas.load_sliced("sb_thumb_v"),
                                         max(0, self.scrolling_container.height),
                                         sb_button_mouseover=assets.gui_atlas.load_sliced("sb_thumb_v_hl"),
                                         on_value_changed_callback=self._on_scroll_changed)

        self.add_child(self.scrolling_container)
        self.add_child(self.vertical_scroll)

        self.layout()

        self.selected_tile_idx = 0

    def _on_scroll_changed(self, new_val):
        self.scrolling_container.offset = make_vector(0, self.vertical_scroll.value)
        #self.scrolling_container.relative_position = make_vector(0, self.vertical_scroll.value)
        self.scrolling_container.layout()

    def _make_selection(self, entity_name):
        print("selected ", entity_name)

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
