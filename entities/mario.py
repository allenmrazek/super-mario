import math
from typing import NamedTuple
import pygame
from pygame import Vector2
from .entity import Entity
from util import mario_str_to_pixel_value as mstpv
import config

frames_to_seconds = 60.  # mario speeds defined in terms of 60 fps
frames_to_seconds_squared = frames_to_seconds ** 2

# horizontal movement constants
min_walk_velocity = frames_to_seconds * mstpv('00130')
max_walk_velocity = frames_to_seconds * mstpv('01900')
max_run_velocity = frames_to_seconds * mstpv('02900')
skid_turnaround_velocity = frames_to_seconds * mstpv('00900')

walking_acceleration = frames_to_seconds_squared * mstpv('00098')
running_acceleration = frames_to_seconds_squared * mstpv('000E4')
release_deceleration = frames_to_seconds_squared * mstpv('000D0')
skid_deceleration = frames_to_seconds_squared * mstpv('001A0')

num_frames_hold_speed = 10

# momentum constants
momentum_velocity_threshold = frames_to_seconds * mstpv('01900')
momentum_start_jump_threshold = frames_to_seconds * mstpv('01D000')

momentum_forward_low = frames_to_seconds_squared * mstpv('00098')
momentum_forward_fast = frames_to_seconds_squared * mstpv('000E4')

momentum_backward_fast = frames_to_seconds_squared * mstpv('000E4')  # used when current speed > velocity threshold
momentum_backward_high_initial_speed = frames_to_seconds_squared * mstpv('000D0')  # low cur speed, high initial
momentum_backward_low_initial_speed = frames_to_seconds_squared * mstpv('00098')  # low cur speed, low initial


# air physics constants
class _JumpParameters(NamedTuple):
    initial_speed: float  # horizontal speed threshold
    initial_velocity_y: float  # mario velocity set to this value when jumping
    jump_button_gravity: float  # gravity applied at this rate when jump button held
    gravity: float  # gravity applied at this rate unless jump button held

    @staticmethod
    def create(i_h_speed, initial_velocity_y, jump_gravity, gravity):
        return _JumpParameters(
            frames_to_seconds * mstpv(i_h_speed),
            frames_to_seconds * mstpv(initial_velocity_y),
            frames_to_seconds_squared * mstpv(jump_gravity),
            frames_to_seconds_squared * mstpv(gravity))


vertical_physics_parameters = [
    _JumpParameters.create('01000', '04000', '00200', '00700'),
    _JumpParameters.create('024FF', '04000', '001E0', '00600'),
    _JumpParameters.create('FFFFF', '05000', '00280', '00900')
]

level_entry_vertical_physics = _JumpParameters.create('00000', '00000', '00280', '00280')

air_max_velocity = frames_to_seconds * mstpv('04800')
air_velocity_when_max_exceeded = frames_to_seconds * mstpv('04000')


class Mario(Entity):
    def __init__(self, input_state):
        super().__init__()
        self.input_state = input_state

        self.image = pygame.image.load("images/mario.png").convert()
        self.rect = self.image.get_rect()

        # state values
        # todo: consider changing from frame counter to delta time, so avoid locking update loop at 1/60 dt
        self.position = Vector2()
        self.velocity = Vector2()
        self.run_frame_counter = 0  # has nothing to do with animation, see ** in smb_playerphysics.png
        self.use_skid_deceleration = False
        self.skidding = False
        self.jump_stats = None
        self.falling_gravity = level_entry_vertical_physics.gravity
        self.jumped = False

        # temp: set initial position of mario
        self.position.x, self.position.y = 0, config.screen_rect.bottom - self.image.get_height() // 2
        self.velocity.x = 0.
        self.run_timer = 0.

    def update(self, dt):
        initial_pos = self.position
        initial_velocity = self.velocity

        if self.is_running and not self.input_state.dash:
            self.run_frame_counter = min(self.run_frame_counter + 1, num_frames_hold_speed + 1)
        else:
            self.run_frame_counter = 0

        # handle horizontal movement
        if self.input_state.left ^ self.input_state.right:
            self._handle_horizontal_acceleration(dt)
        else:
            self._handle_horizontal_deceleration(dt)

        self._handle_vertical_movement(dt)

        # update position based on new velocity calculated by the above
        self.position += self.velocity * dt

        # temp: wraparound screen
        if self.position.x + self.image.get_width() > config.screen_rect.width:
            self.position.x = 0.
            self.velocity.x = 0.

        # temp: floor
        if self.position.y + self.image.get_height() // 2 > config.screen_rect.height:
            # jump is over, reset
            self.position.y = config.screen_rect.height - self.image.get_height() // 2
            self.velocity.y = 0
            self.jump_stats = None

    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.image, self.rect)

    @property
    def collision_mask(self):
        return 0

    def _handle_horizontal_acceleration(self, dt):
        """Left or right is pressed: this means we're accelerating, but direction will determine whether
        Mario skids to a stop or tries to accelerate to his max walk or run speed"""

        acceleration_direction = 1. if self.input_state.right else -1.
        decelerating = True if ((acceleration_direction > 0. and self.velocity.x < 0.) or
                                (acceleration_direction < 0. and self.velocity.x > 0.)) else False

        # note to self: decel and skidding case is to preserve skidding state even as mario's speed
        # drops below running; it'll be reset on either:
        #   1) sucessful turnaround, or
        #   2) user lets go of relevant dir, or changes dir
        self.skidding = decelerating
        self.use_skid_deceleration = self.use_skid_deceleration or self.skidding

        accel = running_acceleration if self.input_state.dash else walking_acceleration
        accel = accel if not self.use_skid_deceleration else skid_deceleration
        accel *= acceleration_direction

        max_velocity = max_run_velocity if self.input_state.dash else max_walk_velocity

        if not self.skidding and not decelerating and self.is_running and not self.input_state.dash:
            # holding dir down, but without dash button
            # maintain run speed for 10 frames, then transition *instantly* to walk
            if self.run_frame_counter > num_frames_hold_speed:
                self.velocity.x = max_walk_velocity * acceleration_direction
            # else: do nothing, maintain speed for 10 frames

        elif self.skidding:  # attempting to accelerate in opposite dir and is or was running
            # special rule for this is that if we reach a certain speed threshold, don't need to slow to a stop
            # before mario's direction changes
            self.velocity.x += accel * dt

            if math.fabs(self.velocity.x) < skid_turnaround_velocity:
                self.velocity.x = 0.
                self.skidding = False
        else:
            # simple case: just apply appropriate acceleration
            self.velocity.x += accel * dt

            # limit max velocity
            if self.velocity.x > max_velocity and not decelerating:
                self.velocity.x = max_velocity
            elif self.velocity.x < -max_velocity:
                self.velocity.x = -max_velocity

            # enforce minimum velocity
            if math.fabs(self.velocity.x) < min_walk_velocity:
                self.velocity.x = min_walk_velocity * acceleration_direction

    def _handle_horizontal_deceleration(self, dt):
        """Handle slowing to a stop; no direction keys are being pressed"""
        self.skidding = False

        if math.fabs(self.velocity.x) > min_walk_velocity:
            # only tricky bit is that if we were skidding but direction didn't change while user was pressing
            # the key (i.e. they released it early, without pressing the opposite direction), then deceleration
            # continues at the skid rate rather than the release rate
            decel = release_deceleration if not self.use_skid_deceleration else skid_deceleration
            delta = -decel * dt if self.velocity.x > 0. else decel * dt

            if self.velocity.x > 0 and self.velocity.x + delta < 0.:
                self.velocity.x = 0.
                self.use_skid_deceleration = False
            elif self.velocity.x < 0 and self.velocity.x + delta > 0.:
                self.velocity.x = 0.
                self.use_skid_deceleration = False
            else:
                self.velocity.x += delta

        else:
            self.use_skid_deceleration = False
            self.velocity.x = 0.

    def _handle_vertical_movement(self, dt):
        """The main tricky bit with this is remember than it's not just jumping that gets mario into the air:
        falling off ledges and enemy impact counts too"""
        # todo: enemy impact physics

        if self.input_state.jump and not self.is_airborne and not self.jumped:
            # jumping just consists of directly setting vertical velocity;
            # the actual velocity depends on mario's horizontal speed ...
            jump_stats = next((js for js in vertical_physics_parameters
                               if math.fabs(self.velocity.x) < js.initial_speed), None)

            assert jump_stats is not None  # likely means velocity got out of control somehow

            self.velocity.y = -jump_stats.initial_velocity_y
            self.falling_gravity = jump_stats.gravity
            self.jumped = True  # flag set to know we should use jump stat gravity, rather than last falling gravity

            # note: the initial horizontal speed when jump began is of interest in mid-air momentum calculations,
            # so copy jump stats and insert current horizontal velocity into it
            self.jump_stats = _JumpParameters(math.fabs(self.velocity.x), *jump_stats[1:])

            return

        # update player vertical physics
        if self.is_airborne:
            if self.jumped:
                assert self.jump_stats

                # holding jump alters gravity, so long as mario is moving upwards
                gravity = self.jump_stats.jump_button_gravity \
                    if self.input_state.jump and self.velocity.y < 0. else self.jump_stats.gravity
            else:  # fell off a ledge, use last falling gravity
                gravity = self.falling_gravity

            self.velocity.y += gravity * dt

            # limit vertical DOWNWARD velocity
            # for some reason it wraps around, kept for sake of authenticity
            self.velocity.y = air_velocity_when_max_exceeded if self.velocity.y > air_max_velocity else self.velocity.y
        else:
            self.jumped = self.jumped and self.input_state.jump

    @property
    def is_running(self):
        """Return true if mario is moving at a running speed"""
        return math.fabs(self.velocity.x) > max_walk_velocity

    @property
    def is_airborne(self):
        """Returns true if mario is in the air"""
        return math.fabs(self.velocity.y) > 0. or \
            self.position.y < config.screen_rect.height - self.image.get_height() // 2.

        # todo: remove y coordinate when collision is implemented
        # note to self: consider that velocity.y == 0 at height of arc
        # which means this is more than just a velocity check
