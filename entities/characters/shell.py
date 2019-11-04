import math
from .projectile import Projectile
from util import mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from .parameters import CharacterParameters
from util import make_vector
from .behaviors import DamageMario
from . import Enemy
import constants

deadly_shell_parameters = CharacterParameters(mstpvv('03500'), mstpvv('04000'), mstpva('00300'), 0., mstpvv('00700'))


class Shell(Projectile):
    # todo: mario stomping shell in motion
    # todo: richochet off pipes
    # todo: don't kill offscreen enemies

    """Deadly version of the shell"""

    def __init__(self, level, direction, shell_animation):
        self.level = level
        self.sounds = level.asset_manager.sounds

        from animation import StaticAnimation

        self.shell = StaticAnimation(shell_animation.image)

        super().__init__(self.shell, level, deadly_shell_parameters, (1, 1), (14, 14),
                         constants.Block, constants.Enemy | constants.Mario)

        self.movement.velocity = make_vector(
            math.copysign(deadly_shell_parameters.max_horizontal_velocity, direction), 0.)

        # state
        self._reverse = False

    def update(self, dt, view_rect):
        # hit something in movement mask
        if self._reverse:
            self.movement.velocity.x *= -1.
            self.sounds['bump'].play()
            self._reverse = False

        super().update(dt, view_rect)

    def on_movement_collision(self, collision):
        if collision.hit_block:
            self._reverse = True

    def on_hit(self, collision):
        # hit something in harm mask
        # is it mario?
        mario = self.level.mario

        if collision.hit_block:
            return

        hit_thing = collision.hit_collider.entity

        if mario is hit_thing:
            # is shell moving towards or away from mario? only harm mario if it's approaching him
            # this allows mario to kick the shell
            # todo: let mario stop the shell by stomping it

            rel_dir = mario.position.x - self.position.x
            deadly_to_mario = (rel_dir < 0 and self.movement.velocity.x < 0.) \
                or (rel_dir > 0 and self.movement.velocity.x > 0.)

            if deadly_to_mario and not mario.is_invincible:
                DamageMario.hurt_mario(self.level, mario)

        elif isinstance(hit_thing, Enemy):
            hit_thing.die()

    @property
    def layer(self):
        return constants.Active
