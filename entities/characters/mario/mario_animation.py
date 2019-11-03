import math
from animation import Animation
from .mario_constants import *
import entities.characters.mario.mario as m


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


class MarioAnimation:
    """This class merely figures out the appropriate mario animation to display"""
    def __init__(self, atlas):
        self.stand = _Variation(
            # small mario variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("mario_stand_left"),
                              atlas.load_static("mario_stand_right")),
                _DirectionSet(atlas.load_static("mario_fire_stand_left"),
                              atlas.load_static("mario_fire_stand_right")),
                None),

            # large mario variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("super_mario_stand_left"),
                              atlas.load_static("super_mario_stand_right")),
                _DirectionSet(atlas.load_static("super_mario_fire_stand_left"),
                              atlas.load_static("super_mario_fire_stand_right")),
                None))

        self.walk = _Variation(
            # small walk variants
            _AnimationSet(
                _DirectionSet(atlas.load_animation("mario_walk_left"),
                              atlas.load_animation("mario_walk_right")),
                _DirectionSet(atlas.load_animation("mario_fire_walk_left"),
                              atlas.load_animation("mario_fire_walk_right")),
                None),

            # super walk variants
            _AnimationSet(
                _DirectionSet(atlas.load_animation("super_mario_walk_left"),
                              atlas.load_animation("super_mario_walk_right")),
                _DirectionSet(atlas.load_animation("super_mario_fire_walk_left"),
                              atlas.load_animation("super_mario_fire_walk_right")),
                None))

        self.run = _Variation(
            # small variants
            _AnimationSet(
                _DirectionSet(atlas.load_animation("mario_run_left"),
                              atlas.load_animation("mario_run_right")),
                _DirectionSet(atlas.load_animation("mario_fire_run_left"),
                              atlas.load_animation("mario_fire_run_right")),
                None),

            # super variants
            _AnimationSet(
                _DirectionSet(atlas.load_animation("super_mario_run_left"),
                              atlas.load_animation("super_mario_run_right")),
                _DirectionSet(atlas.load_animation("super_mario_fire_run_left"),
                              atlas.load_animation("super_mario_fire_run_right")),
                None))

        self.skid = _Variation(
            # small variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("mario_skid_right"),
                              atlas.load_static("mario_skid_left")),
                _DirectionSet(atlas.load_static("mario_fire_skid_right"),
                              atlas.load_static("mario_fire_skid_left")),
                None),

            # super variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("super_mario_skid_right"),
                              atlas.load_static("super_mario_skid_left")),
                _DirectionSet(atlas.load_static("super_mario_fire_skid_right"),
                              atlas.load_static("super_mario_fire_skid_left")),
                None))

        self.jump = _Variation(
            # small variants
            _AnimationSet(_DirectionSet(atlas.load_static("mario_jump_left"),
                                        atlas.load_static("mario_jump_right")),
                          _DirectionSet(atlas.load_static("mario_fire_jump_left"),
                                        atlas.load_static("mario_fire_jump_right")),
                          None),

            # super variants
            _AnimationSet(_DirectionSet(atlas.load_static("super_mario_jump_left"),
                                        atlas.load_static("super_mario_jump_right")),
                          _DirectionSet(atlas.load_static("super_mario_fire_jump_left"),
                                        atlas.load_static("super_mario_fire_jump_right")),
                          None))

        self.crouch = _Variation(
            # super variants (these would be used for small, but that should never happen ...
            # so just use any valid values for the small crouch variation
            _AnimationSet(
                _DirectionSet(atlas.load_static("super_mario_crouch_left"),
                              atlas.load_static("super_mario_crouch_right")),
                _DirectionSet(atlas.load_static("super_mario_fire_crouch_left"),
                              atlas.load_static("super_mario_fire_crouch_right")),
                None),

            # super variants
            _AnimationSet(
                _DirectionSet(atlas.load_static("super_mario_crouch_left"),
                              atlas.load_static("super_mario_crouch_right")),
                _DirectionSet(atlas.load_static("super_mario_fire_crouch_left"),
                              atlas.load_static("super_mario_fire_crouch_right")),
                None))

        self.current = self.stand.small.normal[1]

    @staticmethod
    def _variation_to_set(mario, variations: _Variation):
        variation = variations.super if mario.is_super else variations.small

        # now, which animation set to use will depend on the most significant
        # flag set ..
        if mario.effects & m.MarioEffectStar:
            return variation.normal
            #raise NotImplementedError
        elif mario.effects & m.MarioEffectFire:
            return variation.fire
        else:
            return variation.normal

    def update(self, mario, dt):
        mario_movement = mario.movement
        direction = 1 if mario_movement.is_facing_right else 0

        # airborne?
        if mario_movement.is_airborne:
            self.current = MarioAnimation._variation_to_set(mario, self.jump)[direction]
        else:
            if mario_movement.crouching:
                self.current = MarioAnimation._variation_to_set(mario, self.crouch)[direction]
            elif math.fabs(mario_movement.horizontal_speed) < min_walk_velocity:
                self.current = MarioAnimation._variation_to_set(mario, self.stand)[direction]
            elif mario_movement.is_skidding:
                self.current = MarioAnimation._variation_to_set(mario, self.skid)[direction]
            elif mario_movement.is_running:
                self.current = MarioAnimation._variation_to_set(mario, self.run)[direction]
            else:
                self.current = MarioAnimation._variation_to_set(mario, self.walk)[direction]

        self.current.update(dt)

    @property
    def image(self):
        return self.current.image
