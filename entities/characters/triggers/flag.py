from pygame import Rect
import pygame
from entities.characters import LevelEntity
from ..behaviors import Interactive
from util import world_to_screen
from entities.entity import Layer
from entities.gui.modal.modal_text_input import ModalTextInput
from util import make_vector, rescale_vector


class Flag(LevelEntity):

    def __init__(self, level):
        self.pole = level.asset_manager.interactive_atlas.load_static("flag_pole")
        self.flag = level.asset_manager.interactive_atlas.load_static("flag")
        self.level = level
        self.mario = level.mario
        self.flag_offset = rescale_vector(make_vector(-13, 16))  # from top-left of pole

        super().__init__(self.pole.get_rect())

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        if not self.level.cleared and self.mario.position.x + self.mario.rect.width > self.position.x:
            print("**** flag victory ****")
            self.level.set_cleared()

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.pole.image, world_to_screen(self.position, view_rect))
        screen.blit(self.flag.image, world_to_screen(self.position + self.flag_offset, view_rect))

    def destroy(self):
        self.level.entity_manager.unregister(self)

    def create_preview(self):
        return self.pole.image.copy()

    @property
    def layer(self):
        return Layer.Background


def make_flag(level, values):
    flag = Flag(level)

    if values is not None:
        flag.deserialize(values)

    return flag


LevelEntity.register_factory(Flag, make_flag)
