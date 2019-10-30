from pygame import Rect
import pygame
from entities.characters import LevelEntity
from ..behaviors import Interactive
from util import world_to_screen
from entities.gui.modal.modal_text_input import ModalTextInput
import constants
from util import make_vector


class LevelWarp(LevelEntity):
    SIZE = (64, 64)

    def __init__(self, level):
        self.surface = level.asset_manager.gui_atlas.load_static("level_warp").image
        self.level = level

        font = pygame.font.Font(None, 24)

        self.next_level_file = ""
        self.spawn_idx = 0

        super().__init__(Rect(0, 0, *LevelWarp.SIZE))

        self.trigger = Interactive(level, self, (0, 0), LevelWarp.SIZE, self._change_level)
        self._launch = False

        self.target_text = font.render(self.next_level_file, True, (0, 0, 0), (255, 255, 255))
        self.idx_text = font.render(str(self.spawn_idx), True, (0, 0, 0), (255, 255, 255))

    def _change_level(self, collision):
        self.level.load_from_path("levels/" + self.next_level_file)
        # no need to destroy this entity, it's already removed from the level

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.trigger.update(dt)

        if self._launch:
            self.destroy()
            self.level.load_from_path("levels/" + self.next_level_file)

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        self.trigger.draw(screen, view_rect)

        screen.blit(self.surface, world_to_screen(self.position, view_rect))
        screen.blit(self.target_text, world_to_screen(self.position, view_rect))
        screen.blit(self.idx_text, world_to_screen(self.position + make_vector(0, 20), view_rect))

    def destroy(self):
        self.level.entity_manager.unregister(self)
        self.trigger.destroy()

    def create_preview(self):
        return self.surface.copy()

    @property
    def layer(self):
        return constants.Trigger

    def serialize(self):
        values = super().serialize()

        values['next_level'] = self.next_level_file
        values['spawner_idx'] = self.spawn_idx

        return values

    def deserialize(self, values):
        super().deserialize(values)

        self.next_level_file = values['next_level'] if 'next_level' in values else ''
        self.spawn_idx = int(values['spawner_idx']) if 'spawner_idx' in values else 0

    def spawned_in_editor(self):
        ModalTextInput.spawn(self.level.asset_manager.gui_atlas, "Enter target level",
                             self.on_file_set, self.on_file_cancel)

    def on_file_set(self, text):
        self.next_level_file = text

        ModalTextInput.spawn(self.level.asset_manager.gui_atlas, "Enter spawn location index",
                             self.on_idx_set, self.on_idx_cancel)

    def on_file_cancel(self):
        self.destroy()

    def on_idx_set(self, text):
        self.spawn_idx = int(text)

        font = pygame.font.Font(None, 24)

        self.target_text = font.render(self.next_level_file, True, (0, 0, 0), (255, 255, 255))
        self.idx_text = font.render(str(self.spawn_idx), True, (0, 0, 0), (255, 255, 255))

    def on_idx_cancel(self):
        self.destroy()


def make_level_change(level, values):
    lc = LevelWarp(level)

    if values is not None:
        lc.deserialize(values)

    return lc


LevelEntity.register_factory(LevelWarp, make_level_change)
