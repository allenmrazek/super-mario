from event import PlayerInputHandler
from ..parameters import CharacterParameters
from util import mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from util import make_vector
from ..fireball import Fireball

import constants

fireball_parameters = CharacterParameters(mstpvv('03900'), mstpvv('02400'), mstpva('00300'), mstpvv('02400'), 0.)


class FireballThrow:
    DELAY = 0.25

    def __init__(self, level, input_state):
        super().__init__()

        self.input_state = input_state  # type: PlayerInputHandler
        self.level = level

        # state
        self._fired = False
        self._cooldown = 0.

    def update(self, dt):
        from .mario import MarioEffectFire

        if self.input_state.fire and self.level.mario.enabled and \
                (self.level.mario.effects & MarioEffectFire) == MarioEffectFire and\
                not self.level.mario.movement.crouching:
            if not self._fired and self._cooldown <= 0.:
                self.launch_fireball()
                self._cooldown = FireballThrow.DELAY
                self._fired = True
                return
        elif not self.input_state.fire:
            self._fired = False

        self._cooldown = max(0., self._cooldown - dt)

    def _get_fireball_position(self):
        return self.level.mario.head_position

        # determine where the fireball should appear on mario (depends on direction and size)

    def launch_fireball(self):
        # initial velocity of fireball depends on direction
        initial_velocity = make_vector(fireball_parameters.max_horizontal_velocity, fireball_parameters.max_vertical_velocity)\
            if self.level.mario.movement.is_facing_right else \
            make_vector(-fireball_parameters.max_horizontal_velocity, fireball_parameters.max_vertical_velocity)

        fb = Fireball(self.level, fireball_parameters, initial_velocity)
        fb.position = self._get_fireball_position()

        self.level.entity_manager.register(fb)
        self.level.asset_manager.sounds['fireball'].play()

        self.level.mario.animator.throw()
