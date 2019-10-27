from typing import NamedTuple


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
