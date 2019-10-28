import math
from pygame import Vector2
from entities.characters.mario_constants import *
from entities.entity import Layer
from entities.collider import Collider, ColliderManager
from util import make_vector, copy_vector
from debug.mario_trajectory_visualizer import JumpTrajectoryVisualizer
import config


class MarioMovement:
    def __init__(self, mario_entity, input_state, collider_manager):
        assert mario_entity is not None
        assert input_state is not None
        assert collider_manager is not None

        self.mario_entity = mario_entity
        self.collider_manager = collider_manager
        self.input_state = input_state

        self.debug_trajectory = JumpTrajectoryVisualizer() if config.debug_jumps else None

        # state values
        # todo: consider changing from frame counter to delta time, so avoid locking update loop at 1/60 dt
        self._velocity = Vector2()
        self._run_frame_counter = 0  # has nothing to do with animation, see ** in smb_playerphysics.png
        self._use_skid_deceleration = False
        self._skidding = False
        self._jump_stats = level_entry_vertical_physics
        self._falling_gravity = self._jump_stats.gravity
        self.jumped = False
        self._facing_right = True  # this value is "sticky": if no input, then is dir of last input
        self._airborne = False
        self._enabled = False
        self._position = Vector2()

        # create colliders for mario
        # todo: more accurate collider
        self.collider = Collider.from_entity(mario_entity, self.collider_manager, Layer.Block | Layer.Active)
        self.airborne_collider = Collider.from_entity(mario_entity, self.collider_manager, Layer.Block)

    @property
    def is_running(self):
        """Return true if mario is moving at a running speed"""
        return math.fabs(self._velocity.x) > max_walk_velocity

    @property
    def is_airborne(self):
        """Returns true if mario is in the air. Note that checking velocity by itself is not sufficient: at the top
        of its arc, velocity y component may briefly be 0"""
        return self._airborne

    @property
    def is_facing_right(self):
        return self._facing_right

    @property
    def is_skidding(self):
        return self._skidding

    @property
    def horizontal_speed(self):
        return self._velocity.x

    @property
    def vertical_speed(self):
        return self._velocity.y

    @property
    def rect(self):
        return self.mario_entity.rect

    @property
    def position(self):
        return copy_vector(self.mario_entity.position)

    @position.setter
    def position(self, new_pos):
        self.mario_entity.position = new_pos

    def get_position(self):
        return self.mario_entity.position

    def get_velocity(self):
        return copy_vector(self._velocity)

    def draw(self, screen, view_rect):
        if self.debug_trajectory:
            self.debug_trajectory.draw(screen, view_rect)

    def reset(self):
        # reset parameters besides position
        self._velocity = Vector2()
        self._run_frame_counter = 0
        self._use_skid_deceleration = False
        self._skidding = False
        self._jump_stats = level_entry_vertical_physics
        self._falling_gravity = self._jump_stats.gravity
        self.jumped = False
        self._facing_right = True
        self._airborne = False
        self.collider.position = self.position
        self.airborne_collider.position = self.position

    def update(self, dt, view_rect):
        if self.is_running and not self.input_state.dash:
            self._run_frame_counter = min(self._run_frame_counter + 1, num_frames_hold_speed + 1)
        else:
            self._run_frame_counter = 0

        # handle all vertical movement (gravity and jump are interlinked)
        self._handle_vertical_movement(dt)

        # handle horizontal accelerations
        if self.input_state.left ^ self.input_state.right:
            if self.is_airborne:
                self._handle_horizontal_momentum(dt)
            else:
                self._handle_horizontal_acceleration(dt)
        elif not self.is_airborne:
            self._handle_horizontal_deceleration(dt)

        # updates new horizontal position using velocity calculated from above
        self._handle_horizontal_movement(dt)

        if self.debug_trajectory:
            self.debug_trajectory.update(self, view_rect)

    def _handle_horizontal_acceleration(self, dt):
        """Left or right is pressed: this means we're accelerating, but direction will determine whether
        Mario skids to a stop or tries to accelerate to his max walk or run speed"""

        # ** important note ** this is specifically for ground acceleration. Physics for air
        # momentum are different and use different rules
        acceleration_direction = 1. if self.input_state.right else -1.
        decelerating = True if ((acceleration_direction > 0. and self._velocity.x < 0.) or
                                (acceleration_direction < 0. and self._velocity.x > 0.)) else False

        if self.input_state.right:
            self._facing_right = True
        else:
            self._facing_right = False

        # note to self: decel and skidding case is to preserve skidding state even as mario's speed
        # drops below running; it'll be reset on either:
        #   1) sucessful turnaround, or
        #   2) user lets go of relevant dir, or changes dir
        self._skidding = decelerating
        self._use_skid_deceleration = self._use_skid_deceleration or self._skidding

        accel = running_acceleration if self.input_state.dash else walking_acceleration
        accel = accel if not self._use_skid_deceleration else skid_deceleration
        accel *= acceleration_direction

        max_velocity = max_run_velocity if self.input_state.dash else max_walk_velocity

        if not self._skidding and not decelerating and self.is_running and not self.input_state.dash:
            # holding dir down, but without dash button
            # maintain run speed for 10 frames, then transition *instantly* to walk
            if self._run_frame_counter > num_frames_hold_speed:
                self._velocity.x = max_walk_velocity * acceleration_direction
            # else: do nothing, maintain speed for 10 frames

        elif self._skidding:  # attempting to accelerate in opposite dir and is or was running
            # special rule for this is that if we reach a certain speed threshold, don't need to slow to a stop
            # before mario's direction changes
            self._velocity.x += accel * dt

            if math.fabs(self._velocity.x) < skid_turnaround_velocity:
                self._velocity.x = 0.
                self._skidding = False
        else:
            # simple case: just apply appropriate acceleration
            self._velocity.x += accel * dt

            # limit max velocity
            if self._velocity.x > max_velocity and not decelerating:
                self._velocity.x = max_velocity
            elif self._velocity.x < -max_velocity:
                self._velocity.x = -max_velocity

            # enforce minimum velocity
            if math.fabs(self._velocity.x) < min_walk_velocity:
                self._velocity.x = min_walk_velocity * acceleration_direction

    def _handle_horizontal_momentum(self, dt):
        """Handle mid-air momentum"""
        momentum_direction = 1. if self.input_state.right else -1.
        gaining_momentum = True if (self._velocity.x >= 0. and momentum_direction > 0.) \
            or (self._velocity.x < 0. and momentum_direction < 0) else False

        if gaining_momentum:

            delta_momentum = momentum_forward_slow \
                if math.fabs(self._velocity.x) < momentum_velocity_threshold else momentum_forward_fast

        else:  # losing momentum
            if math.fabs(self._velocity.x) >= momentum_velocity_threshold:
                delta_momentum = momentum_forward_fast
            else:
                # momentum is below threshold, delta now depends on *** initial speed at time of jump ***
                assert self._jump_stats

                delta_momentum = momentum_backward_low_initial_speed \
                    if self._jump_stats.initial_speed < momentum_velocity_threshold \
                    else momentum_backward_high_initial_speed

        delta = delta_momentum * momentum_direction * dt

        if not gaining_momentum and math.fabs(self._velocity.x) < delta:
            self._velocity.x = 0.
        else:
            self._velocity.x += delta

            # limit max horizontal velocity while in mid-air
            max_velocity = momentum_slow_start_max_velocity \
                if self._jump_stats.initial_speed < momentum_velocity_threshold else momentum_fast_start_max_velocity

            if math.fabs(self._velocity.x) > max_velocity:
                self._velocity.x = max_velocity * momentum_direction

    def _handle_horizontal_deceleration(self, dt):
        """Handle slowing to a stop; no direction keys are being pressed"""
        self._skidding = False

        if math.fabs(self._velocity.x) > min_walk_velocity:
            # only tricky bit is that if we were skidding but direction didn't change while user was pressing
            # the key (i.e. they released it early, without pressing the opposite direction), then deceleration
            # continues at the skid rate rather than the release rate
            decel = release_deceleration if not self._use_skid_deceleration else skid_deceleration
            delta = -decel * dt if self._velocity.x > 0. else decel * dt

            if self._velocity.x > 0 and self._velocity.x + delta < 0.:
                self._velocity.x = 0.
                self._use_skid_deceleration = False
            elif self._velocity.x < 0 and self._velocity.x + delta > 0.:
                self._velocity.x = 0.
                self._use_skid_deceleration = False
            else:
                self._velocity.x += delta

        else:
            self._use_skid_deceleration = False
            self._velocity.x = 0.

    def _handle_vertical_movement(self, dt):
        """The main tricky bit with this is to remember that it's not just jumping that gets mario into the air:
        falling off ledges, off disappearing blocks, and enemy impact counts too"""
        # todo: enemy impact physics?

        # determine if mario is airborne: there's at least one pixel downward we can move
        # important note: if mario's velocity actually opposes gravity right now (i.e., negative)
        # then he MUST be airborne
        if self._velocity.y < 0.:
            self._airborne = True
        else:
            # airborne collider is essentially a teleport without movement, no need to update its position
            collisions = self.airborne_collider.test(self.get_position() + make_vector(0, 1))

            if collisions:
                # todo: invoke callbacks for collisions? maybe this should be done in ColliderManager?

                self._airborne = False
                self._velocity.y = 0.
            else:
                self._airborne = True

        # if we're on the ground and haven't already responded to jump, begin a jump
        if self.input_state.jump and not self.is_airborne and not self.jumped:
            # jumping just consists of directly setting vertical velocity;
            # the actual velocity depends on mario's horizontal speed ...
            jump_stats = next((js for js in vertical_physics_parameters
                               if math.fabs(self._velocity.x) < js.initial_speed), None)

            assert jump_stats is not None  # likely means velocity got out of control somehow

            self._velocity.y = -jump_stats.initial_velocity_y
            self._falling_gravity = jump_stats.gravity
            self.jumped = True  # flag set to know we should use jump stat gravity, rather than last falling gravity

            # note: the initial horizontal speed when jump began is of interest in mid-air momentum calculations,
            # so copy jump stats and insert current horizontal velocity into it
            self._jump_stats = JumpParameters(math.fabs(self._velocity.x), *jump_stats[1:])

            return

        # update player vertical physics if mario is already in the air
        if self.is_airborne:
            if self.jumped:
                assert self._jump_stats

                # holding jump alters gravity, so long as mario is moving upwards
                gravity = self._jump_stats.jump_button_gravity \
                    if self.input_state.jump and self._velocity.y < 0. else self._jump_stats.gravity
            else:  # fell off a ledge, use last falling gravity
                gravity = self._falling_gravity

            self._velocity.y += gravity * dt



            #print("gravity = ", gravity)



            # limit vertical DOWNWARD velocity
            # for some reason it wraps around a strange value, kept for sake of authenticity
            self._velocity.y = air_velocity_when_max_exceeded \
                if self._velocity.y > air_max_vertical_velocity else self._velocity.y

            # try and move downward if we can
            # todo: invoke callbacks? or leave that for ColliderManager? collisions ignored for now
            # self.collider.position = self.position
            # target_point = self.position + make_vector(0., self._velocity.y) * dt
            # collisions = self.collider.try_move(target_point)
            #
            # # todo: use approach instead of iterative move
            # if collisions:
            #     dist_moved = self.collider.iterative_move(target_point)
            #     ColliderManager.dispatch_events(self.collider, collisions)
            self.collider.position = self.position
            target_point = self.position + make_vector(0., self._velocity.y) * dt
            self.collider.approach(target_point, True)
            self.position = self.collider.position
        else:
            self.jumped = self.jumped and self.input_state.jump

    def _handle_horizontal_movement(self, dt):
        # horizontal velocity has been calculated, now we just need to apply it
        new_position = make_vector(self._velocity.x * dt, 0.)

        # attempt to move to new position, if we can
        self.collider.position = self.mario_entity.position
        collisions = self.collider.approach(self.mario_entity.position + new_position)
        self.mario_entity.position = self.collider.position

        # todo: handle collision callbacks?

        if collisions:  # immediately stop horizontal movement on horizontal collision
            self._velocity.x = 0.

    def bounce(self, new_y_velocity):
        self._velocity.y = new_y_velocity
