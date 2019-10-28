import math
from enum import IntEnum
from entities.entity import Entity, Layer
from entities.characters.level_entity import LevelEntity
from entities.collider import Collider
from animation import Animation
from util import make_vector, world_to_screen
import config
import entities.characters.behaviors
from .mario_constants import *
from util import rescale_vector


class MarioEffects(IntEnum):
    Small = 0
    Super = 1 << 0
    Fire = 1 << 1
    Star = 1 << 2


class Mario(LevelEntity):
    def __init__(self, input_state, level):
        self.input_state = input_state
        self.cmanager = level.collider_manager
        self.animator = _MarioAnimation(level.asset_manager.character_atlas)
        self.level = level

        super().__init__(self.animator.image.get_rect())
        self.movement = entities.characters.behaviors.MarioMovement(self, self.input_state, self.cmanager)

        self.hitbox = Collider.from_entity(self, self.cmanager, 0)
        self.hitbox.rect.width, self.hitbox.rect.height = rescale_vector(make_vector(10, 14))
        self._hitbox_offset = rescale_vector(make_vector(3, 2))
        self.hitbox.position = self.position + self._hitbox_offset
        self._enabled = False
        self._active_effects = 0

    def update(self, dt, view_rect):
        self.movement.update(dt, view_rect)
        self.animator.update(self, dt)

        self.hitbox.position = self.position + self._hitbox_offset

    def draw(self, screen, view_rect):
        self.movement.draw(screen, view_rect)
        true_pos = world_to_screen(self.rect.topleft, view_rect)
        screen.blit(self.animator.image, true_pos)

        if config.debug_hitboxes:

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

    def bounce(self, new_y_velocity):
        self.movement.bounce(new_y_velocity)

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

    @property
    def velocity(self):
        return self.movement.get_velocity()

    @property
    def effects(self):
        return self._active_effects

    @property
    def is_super(self):
        return self._active_effects & MarioEffects.Super


class _DirectionSet(NamedTuple):
    left: Animation
    right: Animation


class _AnimationSet(NamedTuple):
    normal: _DirectionSet
    fire: _DirectionSet
    star: _DirectionSet


class _Variation(NamedTuple):
    small: _AnimationSet
    super: _AnimationSet


class _MarioAnimation:
    """This class merely figures out the appropriate mario animation to display"""
    def __init__(self, atlas):
        self.stand = _Variation(
            # small mario variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("mario_stand_left"), atlas.load_static("mario_stand_right")),
                _DirectionSet(atlas.load_static("mario_fire_stand_left"), atlas.load_static("mario_fire_stand_right")),
                None),

            # large mario variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("super_mario_stand_left"), atlas.load_static("super_mario_stand_right")),
                _DirectionSet(atlas.load_static("super_mario_fire_stand_left"), atlas.load_static("super_mario_fire_stand_right")),
            None))

        self.walk = _Variation(
            # small walk variants
            _AnimationSet(
                _DirectionSet(atlas.load_animation("mario_walk_left"), atlas.load_animation("mario_walk_right")),
                _DirectionSet(atlas.load_animation("mario_fire_walk_left"), atlas.load_animation("mario_fire_walk_right")),
            None),

            # super walk variants
            _AnimationSet(
                _DirectionSet(atlas.load_animation("super_mario_walk_left"), atlas.load_animation("super_mario_walk_right")),
                _DirectionSet(atlas.load_animation("super_mario_fire_walk_left"), atlas.load_animation("super_mario_fire_walk_right")),
            None))

        self.run = _Variation(
            # small variants
            _AnimationSet(
                _DirectionSet(atlas.load_animation("mario_run_left"), atlas.load_animation("mario_run_right")),
                _DirectionSet(atlas.load_animation("mario_fire_run_left"), atlas.load_animation("mario_fire_run_right")),
                None),

            # super variants
            _AnimationSet(
                _DirectionSet(atlas.load_animation("super_mario_run_left"), atlas.load_animation("super_mario_run_right")),
                _DirectionSet(atlas.load_animation("super_mario_fire_run_left"), atlas.load_animation("super_mario_fire_run_right")),
                None))

        self.skid = _Variation(
            # small variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("mario_skid_right"), atlas.load_static("mario_skid_left")),
                _DirectionSet(atlas.load_static("mario_fire_skid_right"), atlas.load_static("mario_fire_skid_left")),
                None),

            # super variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("super_mario_skid_right"), atlas.load_static("super_mario_skid_left")),
                _DirectionSet(atlas.load_static("super_mario_fire_skid_right"), atlas.load_static("super_mario_fire_skid_left")),
                None))

        self.jump = _Variation(
            # small variants
            _AnimationSet(_DirectionSet(atlas.load_static("mario_jump_left"), atlas.load_static("mario_jump_right")),
                          _DirectionSet(atlas.load_static("mario_fire_jump_left"), atlas.load_static("mario_fire_jump_right")),
                          None),

            # super variants
            _AnimationSet(_DirectionSet(atlas.load_static("super_mario_jump_left"), atlas.load_static("super_mario_jump_right")),
                          _DirectionSet(atlas.load_static("super_mario_fire_jump_left"), atlas.load_static("super_mario_fire_jump_right")),
                          None))

        self.crouch = _Variation(
            # super variants (these would be used for small, but that should never happen ...
            _AnimationSet(
                _DirectionSet(atlas.load_static("super_mario_crouch_left"), atlas.load_static("super_mario_crouch_right")),
                _DirectionSet(atlas.load_static("super_mario_fire_crouch_left"),
                          atlas.load_static("super_mario_fire_crouch_right")),
                None),

            # super variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("super_mario_crouch_left"), atlas.load_static("super_mario_crouch_right")),
                _DirectionSet(atlas.load_static("super_mario_fire_crouch_left"),
                              atlas.load_static("super_mario_fire_crouch_right")),
                None))

        self.current = self.stand.small.normal[1]

    @staticmethod
    def _variation_to_set(mario: Mario, variations: _Variation):
        variation = variations.super if mario.is_super else variations.small

        # now, which animation set to use will depend on the most significant
        # flag set ..
        if mario.effects & MarioEffects.Star:
            #return variation.star
            raise NotImplementedError
        elif mario.effects & MarioEffects.Fire:
            #return variation.fire
            raise NotImplementedError
        else:
            return variation.normal

    def update(self, mario, dt):
        mario_movement = mario.movement
        direction = 1 if mario_movement.is_facing_right else 0

        # airborne?
        if mario_movement.is_airborne:
            #self.current = self.jump[direction]

            self.current = _MarioAnimation._variation_to_set(mario, self.jump)[direction]
        else:
            if math.fabs(mario_movement.horizontal_speed) < min_walk_velocity:
                #self.current = self.stand[direction]
                self.current = _MarioAnimation._variation_to_set(mario, self.stand)[direction]
            elif mario_movement.is_skidding:
                #self.current = self.skid[direction]
                self.current = _MarioAnimation._variation_to_set(mario, self.skid)[direction]
            elif mario_movement.is_running:
                #self.current = self.run[direction]
                self.current = _MarioAnimation._variation_to_set(mario, self.run)[direction]
            elif mario_movement.is_crouching:
                assert mario.effects & MarioEffects.Super
                self.current = _MarioAnimation._variation_to_set(mario, self.crouch)[direction]
            else:
                #self.current = self.walk[direction]
                self.current = _MarioAnimation._variation_to_set(mario, self.walk)[direction]

        self.current.update(dt)

    @property
    def image(self):
        return self.current.image


LevelEntity.register_factory(Mario, Mario.factory)

