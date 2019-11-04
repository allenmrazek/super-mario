from entities.characters import LevelEntity
from util import world_to_screen
from util import make_vector, rescale_vector
from entities.effects.level_cleared import LevelCleared
from state.game_state import state_stack
import constants


class Flag(LevelEntity):

    def __init__(self, level):
        self.pole = level.asset_manager.interactive_atlas.load_static("flag_pole")
        self.flag = level.asset_manager.interactive_atlas.load_static("flag")
        self.level = level
        self.mario = level.mario
        self.flag_offset = rescale_vector(make_vector(-13, 16))  # from top-left of pole
        self.flag_movement = make_vector(0, 0)

        self._pole_height = self.pole.get_rect().height - self.flag_offset.y - self.flag.height

        super().__init__(self.pole.get_rect())

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        if not self.level.cleared and self.mario.position.x + self.mario.rect.width > self.position.x:
            flag_height = self.rect.height
            delta_ground = max(0, self.rect.bottom - self.mario.rect.top)

            ratio = max(0, min(1., delta_ground / flag_height))

            state_stack.push(LevelCleared(self.level, state_stack.top, ratio))

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.pole.image, world_to_screen(self.position, view_rect))
        screen.blit(self.flag.image, world_to_screen(self.position + self.flag_offset + self.flag_movement, view_rect))

    def destroy(self):
        self.level.entity_manager.unregister(self)

    def create_preview(self):
        return self.pole.image.copy()

    @property
    def layer(self):
        return constants.Background

    def set_flag_position(self, fpos):  # as a ratio
        self.flag_movement = make_vector(0, fpos * self._pole_height)


def make_flag(level, values):
    flag = Flag(level)

    if values is not None:
        flag.deserialize(values)

    return flag


LevelEntity.register_factory(Flag, make_flag)
