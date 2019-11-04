from entities.characters.level_entity import LevelEntity
from util import world_to_screen
import entities.characters.behaviors
from .mario_animation import MarioAnimation
from .mario_movement import MarioMovement
from .fireball_throw import FireballThrow

import constants

# plain ints because IntEnum is awful for performance surprisingly
MarioEffectSmall = 0
MarioEffectSuper = 1 << 0
MarioEffectFire = (1 << 1) | MarioEffectSuper  # fire mario has to be super apparently
MarioEffectStar = 1 << 2


class Mario(LevelEntity):
    def __init__(self, input_state, level):
        self.input_state = input_state
        self.cmanager = level.collider_manager
        self.animator = MarioAnimation(level.asset_manager.character_atlas)
        self.level = level

        super().__init__(self.animator.image.get_rect())
        self.movement = MarioMovement(self, self.input_state, self.cmanager,
                                      level.asset_manager.sounds['jump_small'],
                                      level.asset_manager.sounds['jump_super'])
        self.fireballs = FireballThrow(level, input_state)
        self._enabled = False
        #self._active_effects = MarioEffectSmall | MarioEffectFire | MarioEffectSuper | MarioEffectStar
        self._active_effects = MarioEffectStar
        self._invincibility_period = 0.
        self._glued = False

    def update(self, dt, view_rect):
        self.movement.update(dt, view_rect)
        self.animator.update(self, dt)
        self.fireballs.update(dt)

        self._invincibility_period = max(0., self._invincibility_period - dt)

    def draw(self, screen, view_rect):
        true_pos = world_to_screen(self.rect.topleft, view_rect)
        screen.blit(self.animator.image, true_pos)
        self.movement.draw(screen, view_rect)

    def make_invincible(self, period):
        self._invincibility_period = period

    @property
    def layer(self):
        return constants.Mario

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, tf):
        if not tf and self._enabled:
            self.movement.enabled = False
            self._enabled = False
        elif tf and not self._enabled:
            self.movement.enabled = True
            self._enabled = True

    @property
    def glued(self):
        return self._glued

    @glued.setter
    def glued(self, tf):
        self._glued = tf

    def destroy(self):
        self.enabled = False
        self.level.entity_manager.unregister(self)

    def serialize(self):
        values = super().serialize()

        # note to self: don't serialize mario state; that can change between levels
        return values

    def deserialize(self, values):
        super().deserialize(values)

    def create_preview(self):
        return self.animator.image.copy()

    def bounce(self, new_y_velocity):
        self.movement.bounce(new_y_velocity)

    def reset(self):
        self.movement.reset()
        self.glued = False

    @staticmethod
    def factory(level, values):
        mario = Mario(level.player_input, level)

        if values is not None:
            mario.deserialize(values)

        return mario

    @property
    def vertical_speed(self):
        return self.movement.vertical_speed

    @property
    def head_position(self):
        # return coordinates of mario's head in world space
        return self.movement.get_head_position()

    @property
    def velocity(self):
        return self.movement.get_velocity()

    @property
    def effects(self):
        return self._active_effects

    @effects.setter
    def effects(self, effects):
        self._active_effects = effects

    @property
    def is_super(self):
        return self._active_effects & MarioEffectSuper

    @property
    def is_invincible(self):  # note: NOT starman! this is for the invincibility period after taking damage
        return self._invincibility_period > 0.

    @property
    def invincibility_timer(self):
        return self._invincibility_period

    @property
    def is_starman(self):
        return self._active_effects & MarioEffectStar


LevelEntity.register_factory(Mario, Mario.factory)
