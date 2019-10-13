import math
import pygame
from pygame import Vector2
from .entity import Entity
from util import mario_str_to_pixel_value as mstpv
import config

factor = 60.  # mario speeds defined in terms of 60 fps

min_walk_velocity = factor * mstpv('00130')
max_walk_velocity = factor * mstpv('01900')
max_run_velocity = factor * mstpv('02900')
skid_turnaround_velocity = factor * mstpv('00900')

walking_acceleration = factor ** 2 * mstpv('00098')
running_acceleration = factor ** 2 * mstpv('000E4')
release_deceleration = factor ** 2 * mstpv('000D0')
skid_deceleration = factor ** 2 * mstpv('001A0')

num_frames_hold_speed = 10


class Mario(Entity):
    def __init__(self, input_state):
        super().__init__()
        self.input_state = input_state

        self.image = pygame.image.load("images/mario.png").convert()
        self.rect = self.image.get_rect()

        self.position = Vector2()
        self.velocity = Vector2()

        # todo: rather than frame counter, convert to use elapsed time
        self.run_frame_counter = 0  # has nothing to do with animation, see ** in smb_playerphysics.png
        self.use_skid_deceleration = False
        self.skidding = False

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

        # todo: handle vertical movement

        # update position based on new velocity calculated by the above
        self.position += self.velocity * dt

        if self.position.x + self.image.get_width() > config.screen_rect.width:
            self.position.x = 0.
            self.velocity.x = 0.

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

    @property
    def is_running(self):
        """Return true if mario is moving at a running speed"""
        return math.fabs(self.velocity.x) > max_walk_velocity
