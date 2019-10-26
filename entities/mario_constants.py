from typing import NamedTuple
import config
from util import mario_str_to_pixel_value as mstpv


frames_to_seconds = 60.  # mario speeds defined in terms of 60 fps with original resolution
frames_to_seconds_squared = frames_to_seconds ** 2

frames_to_seconds *= config.rescale_factor  # apply any scaling factor, so proportions are kept
frames_to_seconds_squared *= config.rescale_factor

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

momentum_forward_slow = frames_to_seconds_squared * mstpv('00098')
momentum_forward_fast = frames_to_seconds_squared * mstpv('000E4')

momentum_backward_fast = frames_to_seconds_squared * mstpv('000E4')  # used when current speed > velocity threshold
momentum_backward_high_initial_speed = frames_to_seconds_squared * mstpv('000D0')  # low cur speed, high initial
momentum_backward_low_initial_speed = frames_to_seconds_squared * mstpv('00098')  # low cur speed, low initial

momentum_slow_start_max_velocity = frames_to_seconds * mstpv('01900')
momentum_fast_start_max_velocity = frames_to_seconds * mstpv('02900')


# air physics constants
class JumpParameters(NamedTuple):
    initial_speed: float  # horizontal speed threshold
    initial_velocity_y: float  # mario velocity set to this value when jumping
    jump_button_gravity: float  # gravity applied at this rate when jump button held
    gravity: float  # gravity applied at this rate unless jump button held

    @staticmethod
    def create(i_h_speed, initial_velocity_y, jump_gravity, gravity):
        return JumpParameters(
            frames_to_seconds * mstpv(i_h_speed),
            frames_to_seconds * mstpv(initial_velocity_y),
            frames_to_seconds_squared * mstpv(jump_gravity),
            frames_to_seconds_squared * mstpv(gravity))


vertical_physics_parameters = [
    JumpParameters.create('01000', '04000', '00200', '00700'),
    JumpParameters.create('024FF', '04000', '001E0', '00600'),
    JumpParameters.create('FFFFF', '05000', '00280', '00900')
]

level_entry_vertical_physics = JumpParameters.create('00000', '00000', '00280', '00280')

air_max_vertical_velocity = frames_to_seconds * mstpv('04800')
air_velocity_when_max_exceeded = frames_to_seconds * mstpv('04000')