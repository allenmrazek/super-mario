from entities.characters.enemy import Enemy
from .damage_mario import DamageMario
from .interactive import Interactive
from entities.collider import Collision, Collider
from ..mario import Mario
from util import make_vector


class Squashable(DamageMario):
    """Essentially a source for a callback when mario lands on top of a hitbox. If he moves into
    the hitbox in another way, Mario is damaged instead"""

    def __init__(self, level, entity, hitbox_offset, hitbox_size, bounce_velocity, squash_callback):
        super().__init__(level, entity, hitbox_offset, hitbox_size)

        assert squash_callback is not None

        self._squashed = False

        self.bounce_velocity = bounce_velocity
        self.on_squashed = squash_callback

    @property
    def squashed(self):
        return self._squashed

    def on_mario_collision(self, collision: Collision):
        # if mario has a positive velocity (moving downwards at all), squash this entity
        # this might seem odd (shouldn't mario be above the enemy?), but based on research
        # this is how original SMB does this

        if self.squashed:
            return

        assert collision.hit_collider is not None
        assert collision.moved_collider is not None

        mario_collider = collision.hit_collider  # type: Collider
        enemy_collider = collision.moved_collider  # type: Collider

        assert isinstance(mario_collider.entity, Mario)
        assert isinstance(enemy_collider.entity, Enemy)

        mario = mario_collider.entity  # type: Mario

        if mario.vertical_speed > 0.:
            self._squashed = True
            self.on_squashed()

            mario.bounce(-self.bounce_velocity)
        else:
            super().on_mario_collision(collision)

    def destroy(self):
        pass
