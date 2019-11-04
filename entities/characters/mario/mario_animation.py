import math
import pygame
from animation import Animation
from .mario_constants import *
import entities.characters.mario.mario as m
import config


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


def generate_frame(surface, factor):
    new_surface = surface.copy()

    with pygame.PixelArray(new_surface) as pixels:
        for y in range(new_surface.get_height()):
            for x in range(new_surface.get_width()):
                clr = new_surface.unmap_rgb(pixels[x][y])

                if clr == config.transparent_color:
                    continue

                clr.r = min(max(0, int(clr.r * factor)), 255)
                clr.g = min(max(0, int(clr.g * factor)), 255)
                clr.b = min(max(0, int(clr.b * factor)), 255)

                pixels[x][y] = new_surface.map_rgb(clr)

    return new_surface.convert()


# cutting out the sprites one by one would be very tedious, so let's be la..efficient and just make
# the colors all crazy based on an existing mario animation set and variation
def generate_starman_animation(animation):
    # create 3 frames for every animation frame, changing its pixels a bunch each time
    frames = []

    factors = [0.65, 0.75, 1.5]
    for val in factors:
        for frame in animation.frames:
            frames.append(generate_frame(frame, val))

    duration = animation.duration * 3 if animation.duration > 0 else 0.125

    return Animation(frames, duration)


def generate_starman_direction_set(from_set):
    return _DirectionSet(generate_starman_animation(from_set.left), generate_starman_animation(from_set.right))

# creating these is expensive, so only do it once
stand_small = None
stand_fire_small = None
stand_starman_small = None
stand_super = None
stand_fire_super = None
stand_starman_super = None

walk_small = None
walk_fire_small = None
walk_starman_small = None
walk_super = None
walk_fire_super = None
walk_starman_super = None

run_small = None
run_fire_small = None
run_starman_small = None
run_super = None
run_fire_super = None
run_starman_super = None

jump_small = None
jump_fire_small = None
jump_starman_small = None
jump_super = None
jump_fire_super = None
jump_starman_super = None

crouch_super = None
crouch_fire_super = None
crouch_starman_super = None

skid_small = None
skid_fire_small = None
skid_starman_small = None
skid_super = None
skid_fire_super = None
skid_starman_super = None


class MarioAnimation:
    SUPER_FIRE_THROW_DURATION = 0.075

    """This class merely figures out the appropriate mario animation to display"""
    def __init__(self, atlas):
        self.fire_throw = atlas.load_static("super_mario_fire_throw_left"), \
                          atlas.load_static("super_mario_fire_throw_right")

        self.throw_timer = 0.
        self.throw_image = self.fire_throw[0]

        global stand_small
        global stand_fire_small
        global stand_starman_small
        global stand_super
        global stand_fire_super
        global stand_starman_super

        global walk_small
        global walk_fire_small
        global walk_starman_small
        global walk_super
        global walk_fire_super
        global walk_starman_super

        global run_small
        global run_fire_small
        global run_starman_small
        global run_super
        global run_fire_super
        global run_starman_super

        global jump_small
        global jump_fire_small
        global jump_starman_small
        global jump_super
        global jump_fire_super
        global jump_starman_super

        global crouch_super
        global crouch_fire_super
        global crouch_starman_super

        global skid_small
        global skid_fire_small
        global skid_starman_small
        global skid_super
        global skid_fire_super
        global skid_starman_super

        ##################### Standing #####################
        # small mario variants
        stand_small = stand_small or _DirectionSet(atlas.load_static("mario_stand_left"), atlas.load_static("mario_stand_right"))
        stand_fire_small = stand_fire_small or _DirectionSet(atlas.load_static("mario_fire_stand_left"),
                              atlas.load_static("mario_fire_stand_right"))
        stand_starman_small = stand_starman_small or generate_starman_direction_set(stand_small)

        # large stand variants
        stand_super = stand_super or _DirectionSet(atlas.load_static("super_mario_stand_left"),
                                    atlas.load_static("super_mario_stand_right"))
        stand_fire_super = stand_fire_super or _DirectionSet(atlas.load_static("super_mario_fire_stand_left"),
                              atlas.load_static("super_mario_fire_stand_right"))
        stand_starman_super = stand_starman_super or generate_starman_direction_set(stand_super)

        self.stand = _Variation(
            _AnimationSet(stand_small, stand_fire_small, stand_starman_small),
            _AnimationSet(stand_super, stand_fire_super, stand_starman_super)
        )

        ################### Walking ####################
        # small walk variants
        walk_small = walk_small or _DirectionSet(atlas.load_animation("mario_walk_left"), atlas.load_animation("mario_walk_right"))
        walk_fire_small = walk_fire_small or _DirectionSet(atlas.load_animation("mario_fire_walk_left"),
                              atlas.load_animation("mario_fire_walk_right"))
        walk_starman_small = walk_starman_small or generate_starman_direction_set(walk_small)

        # super walk variants
        walk_super = walk_super or _DirectionSet(atlas.load_animation("super_mario_walk_left"),
                              atlas.load_animation("super_mario_walk_right"))
        walk_fire_super = walk_fire_super or _DirectionSet(atlas.load_animation("super_mario_fire_walk_left"),
                              atlas.load_animation("super_mario_fire_walk_right"))
        walk_starman_super = walk_starman_super or generate_starman_direction_set(walk_super)

        self.walk = _Variation(
            _AnimationSet(walk_small, walk_fire_small, walk_starman_small),
            _AnimationSet(walk_super, walk_fire_super, walk_starman_super)
        )

        ################### Running ####################
        run_small = run_small or _DirectionSet(atlas.load_animation("mario_run_left"), atlas.load_animation("mario_run_right"))
        run_fire_small = run_fire_small or _DirectionSet(atlas.load_animation("mario_fire_run_left"),
                                  atlas.load_animation("mario_fire_run_right"))
        run_starman_small = run_starman_small or generate_starman_direction_set(run_small)

        run_super = run_super or _DirectionSet(atlas.load_animation("super_mario_run_left"),
                                  atlas.load_animation("super_mario_run_right"))
        run_fire_super = run_fire_super or _DirectionSet(atlas.load_animation("super_mario_fire_run_left"),
                                       atlas.load_animation("super_mario_fire_run_right"))
        run_starman_super = run_starman_super or generate_starman_direction_set(run_super)

        self.run = _Variation(
            _AnimationSet(run_small, run_fire_small, run_starman_small),
            _AnimationSet(run_super, run_fire_super, run_starman_super)
        )

        ################### Skidding ####################
        skid_small = skid_small or _DirectionSet(atlas.load_static("mario_skid_right"), atlas.load_static("mario_skid_left"))
        skid_fire_small = skid_fire_small or _DirectionSet(atlas.load_static("mario_fire_skid_right"), atlas.load_static("mario_fire_skid_left"))
        skid_starman_small = skid_starman_small or generate_starman_direction_set(skid_small)

        skid_super = skid_super or _DirectionSet(atlas.load_static("super_mario_skid_right"),
                              atlas.load_static("super_mario_skid_left"))
        skid_fire_super = skid_fire_super or _DirectionSet(atlas.load_static("super_mario_fire_skid_right"),
                              atlas.load_static("super_mario_fire_skid_left"))
        skid_starman_super = skid_starman_super or generate_starman_direction_set(skid_super)

        self.skid = _Variation(
            _AnimationSet(skid_small, skid_fire_small, skid_starman_small),
            _AnimationSet(skid_super, skid_fire_super, skid_starman_super)
        )

        ################### Jumping ####################
        jump_small = jump_small or _DirectionSet(atlas.load_static("mario_jump_left"),
                                        atlas.load_static("mario_jump_right"))
        jump_fire_small = jump_fire_small or _DirectionSet(atlas.load_static("mario_fire_jump_left"),
                                        atlas.load_static("mario_fire_jump_right"))
        jump_starman_small = jump_starman_small or generate_starman_direction_set(jump_small)

        jump_super = jump_super or _DirectionSet(atlas.load_static("super_mario_jump_left"),
                                        atlas.load_static("super_mario_jump_right"))
        jump_fire_super = jump_fire_super or _DirectionSet(atlas.load_static("super_mario_fire_jump_left"),
                                        atlas.load_static("super_mario_fire_jump_right"))
        jump_starman_super = jump_starman_super or generate_starman_direction_set(jump_super)

        self.jump = _Variation(
            _AnimationSet(jump_small, jump_super, jump_starman_small),
            _AnimationSet(jump_super, jump_fire_super, jump_starman_super)
        )

        ################### Crouching ####################
        crouch_super = crouch_super or _DirectionSet(atlas.load_static("super_mario_crouch_left"),
                              atlas.load_static("super_mario_crouch_right"))
        crouch_fire_super = crouch_fire_super or _DirectionSet(atlas.load_static("super_mario_fire_crouch_left"),
                              atlas.load_static("super_mario_fire_crouch_right"))
        crouch_starman_super = crouch_starman_super or generate_starman_direction_set(crouch_super)

        self.crouch = _Variation(
            # super variants (these would be used for small, but that should never happen ...
            # so just use any valid values for the small crouch variation
            _AnimationSet(crouch_super, crouch_fire_super, crouch_starman_super),
            _AnimationSet(crouch_super, crouch_fire_super, crouch_starman_super)
        )

        self.current = self.stand.small.normal[1]

    @staticmethod
    def _variation_to_set(mario, variations: _Variation):
        variation = variations.super if mario.is_super else variations.small

        # now, which animation set to use will depend on the most significant
        # flag set ..
        if mario.effects & m.MarioEffectStar == m.MarioEffectStar:
            return variation.star
        elif mario.effects & m.MarioEffectFire == m.MarioEffectFire:
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

        self.throw_timer = max(0., self.throw_timer - dt)
        if not mario.is_super:
            self.throw_timer = 0.  # can't throw fireballs unless super at the least

        self.throw_image = self.fire_throw[0] if direction == 0 else self.fire_throw[1]
        self.current.update(dt)

    @property
    def image(self):
        return self.throw_image.image if self.throw_timer > 0. else self.current.image

    def throw(self):
        self.throw_timer = MarioAnimation.SUPER_FIRE_THROW_DURATION
