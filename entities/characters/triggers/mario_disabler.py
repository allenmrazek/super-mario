from pygame import Rect
import pygame
from entities.characters import LevelEntity
from ..behaviors import Interactive
from util import world_to_screen
from entities.gui.modal.modal_text_input import ModalTextInput
from util import make_vector, rescale_vector, world_to_screen
from entities.effects.level_cleared import LevelCleared
from state.game_state import state_stack
from ..behaviors import Interactive
from ..mario import Mario
import config
import constants


class MarioDisabler(LevelEntity):
    SIZE = (64, 64)

    def __init__(self, level):
        self.bulb = level.asset_manager.gui_atlas.load_static("bulb")
        self.level = level

        super().__init__(pygame.Rect(0, 0, *MarioDisabler.SIZE))

        self.trigger = Interactive(level, self, (0, 0), (64, 64), self._on_hit_mario)

    def _on_hit_mario(self, collision):
        if collision.hit_collider and isinstance(collision.hit_collider.entity, Mario):
            collision.hit_collider.entity.enabled = False
            self.destroy()

    def update(self, dt, view_rect):
        self.trigger.update(dt)

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)
        screen.blit(self.bulb.image, world_to_screen(self.position, view_rect))

        if config.debug_hitboxes:
            r = self.rect.copy()
            r.topleft = world_to_screen(self.position, view_rect)
            screen.fill((0, 255, 0), r)

    def destroy(self):
        self.level.entity_manager.unregister(self)

    def create_preview(self):
        return self.bulb.image.copy()

    @property
    def layer(self):
        return constants.Trigger


def make_disabler(level, values):
    disabler = MarioDisabler(level)

    if values is not None:
        disabler.deserialize(values)

    return disabler


LevelEntity.register_factory(MarioDisabler, make_disabler)