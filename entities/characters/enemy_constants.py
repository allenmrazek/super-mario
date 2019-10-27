from typing import NamedTuple
from util import mario_str_to_pixel_value as mstpv


class EnemyParameters(NamedTuple):
    max_horizontal_velocity: float
    max_vertical_velocity: float
    jump_velocity: float
    squash_bounce_velocity: float  # velocity applied to mario when he squashes this enemy (if he can)
    gravity: float

    @staticmethod
    def create(hmax, vmax, jump, squash, gravity):
        return EnemyParameters(max_horizontal_velocity=hmax,
                               max_vertical_velocity=vmax,
                               jump_velocity=jump,
                               squash_bounce_velocity=squash,
                               gravity=gravity)


# todo: pull these out into common file
frames_to_seconds = 60.  # mario speeds defined in terms of 60 fps with original resolution
frames_to_seconds_squared = frames_to_seconds ** 2

# Goomba
goomba_parameters = EnemyParameters.create(100, 100, 100, 100, mstpv('00600') * frames_to_seconds_squared)
