from pygame import Rect
import pygame
from entities.characters import LevelEntity
from ..behaviors import Interactive
from util import world_to_screen
from entities.entity import Layer
from entities.gui.modal.modal_text_input import ModalTextInput
from util import make_vector, rescale_vector
from entities.effects.level_cleared import LevelCleared
from state.game_state import state_stack
from ..behaviors import Interactive


class MarioDisabler(LevelEntity):
    SIZE = (32, 32)

    def __init__(self, level):
        self.bulb = level.asset_manager.gui_atlas.load_static("bulb")
        self.level = level

        super().__init__(pygame.Rect(0, 0, *MarioDisabler.SIZE))

        self.trigger = Interactive(level, self, (0, 0), (32, 32), self._on_hit_mario)

    def _on_hit_mario(self):
        print("disabler hit mario!")

    def update(self, dt, view_rect):
        pass

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

    def destroy(self):
        self.level.entity_manager.unregister(self)

    def create_preview(self):
        return self.bulb.image.copy()

    @property
    def layer(self):
        return Layer.Trigger


def make_disabler(level, values):
    disabler = MarioDisabler(level)

    if values is not None:
        disabler.deserialize(values)

    return disabler


LevelEntity.register_factory(MarioDisabler, make_disabler)