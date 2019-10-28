import math
from entities.entity import Entity, Layer
from entities.characters.level_entity import LevelEntity
from entities.collider import Collider
from animation import Animation
from util import make_vector, world_to_screen
import config
import entities.characters.behaviors
from .mario_constants import *


class Mario(LevelEntity):
    def __init__(self, input_state, level):
        self.input_state = input_state
        self.cmanager = level.collider_manager
        self.animator = _MarioAnimation(level.asset_manager.character_atlas)
        self.level = level

        super().__init__(self.animator.image.get_rect())
        self.movement = entities.characters.behaviors.MarioMovement(self, self.input_state, self.cmanager)

        self.hitbox = Collider.from_entity(self, self.cmanager, 0)
        self.hitbox.rect.width, self.hitbox.rect.height = 10 * config.rescale_factor, 14 * config.rescale_factor
        self.hitbox.position = self.position + make_vector(3 * config.rescale_factor, 2 * config.rescale_factor)

        self._enabled = False

    def update(self, dt, view_rect):
        self.movement.update(dt, view_rect)
        self.animator.update(self.movement, dt)

    def draw(self, screen, view_rect):
        self.movement.draw(screen, view_rect)
        true_pos = world_to_screen(self.rect.topleft, view_rect)
        screen.blit(self.animator.image, true_pos)

        if config.debug_hitboxes:
            self.hitbox.position = self.position + make_vector(3 * config.rescale_factor, 2 * config.rescale_factor)
            r = self.hitbox.rect.copy()
            # todo: factor hitbox out of mario

            r.topleft = world_to_screen(self.hitbox.position, view_rect)
            r = screen.get_rect().clip(r)
            screen.fill((0, 255, 0), r)

    @property
    def layer(self):
        return Layer.Mario

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, tf):
        if not tf and self._enabled:
            self.cmanager.unregister(self.hitbox)
            self._enabled = False
        elif tf and not self._enabled:
            self.cmanager.register(self.hitbox)
            self._enabled = True

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

    def bounce(self, new_velocity):
        self.movement.velocity = new_velocity

    def reset(self):
        self.movement.reset()
        self.hitbox.position = self.position

    @staticmethod
    def factory(level, values):
        mario = Mario(level.player_input, level)

        if values is not None:
            mario.deserialize(values)

        return mario

    @property
    def vertical_speed(self):
        return self.movement.vertical_speed


class _DirectionSet(NamedTuple):
    left: Animation
    right: Animation


class _MarioAnimation:
    """This class merely figures out the appropriate mario animation to display"""
    def __init__(self, atlas):
        self.stand = _DirectionSet(atlas.load_static("mario_stand_left"), atlas.load_static("mario_stand_right"))
        self.walk = _DirectionSet(atlas.load_animation("mario_walk_left"), atlas.load_animation("mario_walk_right"))
        self.run = _DirectionSet(atlas.load_animation("mario_run_left"), atlas.load_animation("mario_run_right"))
        self.skid = _DirectionSet(atlas.load_static("mario_skid_right"), atlas.load_static("mario_skid_left"))
        self.jump = _DirectionSet(atlas.load_static("mario_jump_left"), atlas.load_static("mario_jump_right"))

        self.current = self.stand[1]

    def update(self, mario_movement, dt):
        direction = 1 if mario_movement.is_facing_right else 0

        # airborne?
        if mario_movement.is_airborne:
            self.current = self.jump[direction]
        else:
            if math.fabs(mario_movement.horizontal_speed) < min_walk_velocity:
                self.current = self.stand[direction]
            elif mario_movement.is_skidding:
                self.current = self.skid[direction]
            elif mario_movement.is_running:
                self.current = self.run[direction]
            else:
                self.current = self.walk[direction]

        self.current.update(dt)

    @property
    def image(self):
        return self.current.image


LevelEntity.register_factory(Mario, Mario.factory)

