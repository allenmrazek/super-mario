from .behavior import Behavior
from util import make_vector, copy_vector
from entities.collider import Collider
import constants


class GravityMovement(Behavior):
    """Applies gravity motion only; does not affect horizontal velocity. This should be combined with some type of
    horizontal movement behavior because it does not register a collider in the world and thus is not interactive
    by itself"""
    def __init__(self, entity, collider_manager, gravity_params):
        assert entity is not None
        assert collider_manager is not None

        super().__init__()

        self.entity = entity
        self.collider_manager = collider_manager
        self.velocity = make_vector(0., 0.)
        self.parameters = gravity_params

        self.airborne_collider = Collider.from_entity(entity, collider_manager, constants.Block)

        # private state
        self._airborne = False

    def destroy(self):
        pass  # didn't register any colliders, don't need to do anything

    @property
    def is_airborne(self):
        return self._airborne

    @property
    def velocity(self):
        return self.entity.velocity or make_vector(0, 0)

    @velocity.setter
    def velocity(self, val):
        self.entity.velocity = copy_vector(val)

    def update(self, dt):
        self._handle_vertical_movement(dt)

    def draw(self, screen, view_rect):
        pass

    def _handle_vertical_movement(self, dt):
        self._airborne = self.velocity.y < 0. or not any(
            self.airborne_collider.test(self.entity.position + make_vector(0, 1)))

        current_velocity = self.velocity

        if not self._airborne:
            current_velocity.y = 0
        else:
            current_velocity.y += (self.parameters.gravity * dt)

            # limit downward velocity
            if current_velocity.y > self.parameters.max_vertical_velocity:
                current_velocity.y = self.parameters.max_vertical_velocity

        vel = make_vector(0, current_velocity.y)
        target_pos = self.entity.position + vel * dt
        self.airborne_collider.position = self.entity.position
        self.velocity = current_velocity

        # very important to be accurate with vertical movement because of the single pixel downward we use
        # for airborne detection.
        if any(self.airborne_collider.try_move(target_pos, True)):
            self.airborne_collider.approach(target_pos)
            self._airborne = False

        self.entity.position = self.airborne_collider.position
