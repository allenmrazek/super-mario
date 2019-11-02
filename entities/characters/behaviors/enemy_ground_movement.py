from . import SimpleMovement
import constants
from util import make_vector


class EnemyGroundMovement(SimpleMovement):
    """Moves to the left by default unless it hits a block or other enemy, upon which it reverses direction"""
    def __init__(self, entity, collider_manager, parameters):
        super().__init__(entity, collider_manager, parameters, on_collision_callback=self.on_hit)

        # initially move left at max speed
        self.velocity = make_vector(-parameters.max_horizontal_velocity, 0.)

        # state
        self._reverse_direction = False

    def update(self, dt):
        if self._reverse_direction:
            self.velocity.x *= -1.
            self._reverse_direction = False

        super().update(dt)

    def on_hit(self, collision):
        # note: don't update velocity inside here: it's quite possible multiple collisions have occurred
        # in the same frame, and if two enemies are very close together, they might end up fighting to
        # change direction over and over
        if collision.hit_block:
            # we hit a block, but it could have been from above. Determine if block is left or right
            is_left = any(self.horizontal_movement_collider.test(
                self.horizontal_movement_collider.position - make_vector(1, 0)))
            is_right = any(self.horizontal_movement_collider.test(
                self.horizontal_movement_collider.position + make_vector(1, 0)))

            # only flip directions if it will improve situation
            if (is_left and self.velocity.x < 0.) or (is_right and self.velocity.x > 0.):
                self._reverse_direction = True
        elif collision.hit_collider is not None and collision.hit_collider.layer == constants.Enemy:
            self._reverse_direction = True
