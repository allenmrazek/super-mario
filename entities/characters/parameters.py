from typing import NamedTuple


class CharacterParameters(NamedTuple):
    max_horizontal_velocity: float
    max_vertical_velocity: float
    gravity: float
    jump_velocity: float
    squash_bounce_velocity: float  # velocity applied to mario when he squashes this thing (if he can)
