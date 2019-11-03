import math
from .enemy_ground_movement import EnemyGroundMovement
from entities.collider import Collider
import constants
from util import make_vector


class SmartEnemyGroundMovement(EnemyGroundMovement):
    """Patrols for a certain range and doesn't suicide off of ledges"""
    def __init__(self, entity, collider_manager, parameters, patrol_range):
        super().__init__(entity, collider_manager, parameters)

        self.patrol_range = patrol_range

        # set up edge detection collider
        self.edge_detector = Collider.from_entity(entity, collider_manager, constants.Block)
        self._left_offset = make_vector(-self.entity.rect.width, 1)
        self._right_offset = make_vector(self.entity.rect.width, 1)

        # state
        self._patrolled = 0.

    def update(self, dt):
        # will we fall if we move a body length in the direction of movement?
        offset = self._left_offset if self.velocity.x < 0. else self._right_offset

        if self._patrolled > self.patrol_range or not self.edge_detector.test(self.entity.position + offset):
            # flip direction
            self.velocity *= -1.
            self._patrolled = 0.

        super().update(dt)

        self._patrolled += math.fabs(self.velocity.x * dt)
