from typing import NamedTuple
from util import mario_str_to_pixel_value_velocity as mstpv_velocity
from util import mario_str_to_pixel_value_acceleration as mstpv_accel

# horizontal movement constants
min_walk_velocity = mstpv_velocity('00130')
max_walk_velocity = mstpv_velocity('01900')
max_run_velocity = mstpv_velocity('02900')
skid_turnaround_velocity = mstpv_velocity('00900')

walking_acceleration = mstpv_accel('00098')
running_acceleration = mstpv_accel('000E4')
release_deceleration = mstpv_accel('000D0')
skid_deceleration = mstpv_accel('001A0')

num_frames_hold_speed = 10

# momentum constants
momentum_velocity_threshold = mstpv_velocity('01900')
momentum_start_jump_threshold = mstpv_velocity('01D000')

momentum_forward_slow = mstpv_accel('00098')
momentum_forward_fast = mstpv_accel('000E4')

momentum_backward_fast = mstpv_accel('000E4')  # used when current speed > velocity threshold
momentum_backward_high_initial_speed = mstpv_accel('000D0')  # low cur speed, high initial
momentum_backward_low_initial_speed = mstpv_accel('00098')  # low cur speed, low initial

momentum_slow_start_max_velocity = mstpv_velocity('01900')
momentum_fast_start_max_velocity = mstpv_velocity('02900')


# air physics constants
class JumpParameters(NamedTuple):
    initial_speed: float  # horizontal speed threshold
    initial_velocity_y: float  # mario velocity set to this value when jumping
    jump_button_gravity: float  # gravity applied at this rate when jump button held
    gravity: float  # gravity applied at this rate unless jump button held

    @staticmethod
    def create(i_h_speed, initial_velocity_y, jump_gravity, gravity):
        return JumpParameters(
            mstpv_velocity(i_h_speed),
            mstpv_velocity(initial_velocity_y),
            mstpv_accel(jump_gravity),
            mstpv_accel(gravity))


vertical_physics_parameters = [
    JumpParameters.create('01000', '04300', '00200', '00700'),  # todo: original yinit values are slightly too small,
    JumpParameters.create('024FF', '04300', '001E0', '00600'),  # need to investigate if time
    JumpParameters.create('FFFFF', '05600', '00280', '00900')
]

level_entry_vertical_physics = JumpParameters.create('00000', '00000', '00280', '00280')

air_max_vertical_velocity = mstpv_velocity('04800')
air_velocity_when_max_exceeded = mstpv_velocity('04000')
