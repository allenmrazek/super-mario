from .behavior import Behavior
from util import make_vector
from entities.characters.level_entity import MovementParameters
from entities.collider import Collider
from entities import Layer


class SimpleMovement(Behavior):
    """Side-to-side movement, moving left initially, changes direction on hitting an enemy or block
    (to left or right)"""
    def __init__(self, entity, collider_manager, parameters, movement_collider=None):
        assert entity is not None
        assert collider_manager is not None
        assert parameters is not None

        super().__init__()

        self.entity = entity
        self.collider_manager = collider_manager

        self.movement_collider = movement_collider or Collider.from_entity(entity,
                                                                           collider_manager, Layer.Block | Layer.Enemy)
        self.parameters = parameters  # type: MovementParameters
        self.velocity = make_vector(-self.parameters.max_horizontal_velocity, 0.)

        self.airborne_collider = Collider.from_entity(entity, collider_manager, Layer.Block)

        existing = self.movement_collider.on_collision

        def _wrap(collision):
            if existing is not None:
                existing(collision)
            self._on_hit(collision)

        self.movement_collider.on_collision = _wrap

        # allow other things to collider with our movement collider. Note they
        # must have a mask that hits Layer.Enemy to do this
        collider_manager.register(self.movement_collider)

        # private state
        self._airborne = False
        self._reverse_direction = False

    def finish(self):
        self.collider_manager.unregister(self.movement_collider)

    def destroy(self):
        self.finish()

    @property
    def is_airborne(self):
        return self._airborne

    def update(self, dt):
        self._handle_vertical_movement(dt)
        self._handle_horizontal_movement(dt)

        if self._reverse_direction:
            self.velocity.x *= -1.
            self._reverse_direction = False

    def draw(self, screen, view_rect):
        pass

    def _handle_vertical_movement(self, dt):
        # todo: what if it jumps onto another enemy?
        if self._reverse_direction:
            self._reverse_direction = False
            self.velocity.x *= -1.

        self._airborne = self.velocity.y < 0. or not any(
            self.airborne_collider.test(self.entity.position + make_vector(0, 1)))

        if not self._airborne:
            self.velocity.y = 0
        else:
            self.velocity.y += (self.parameters.gravity * dt)

            # limit downward velocity
            if self.velocity.y > self.parameters.max_vertical_velocity:
                self.velocity.y = self.parameters.max_vertical_velocity

        vel = make_vector(0, self.velocity.y)
        target_pos = self.entity.position + vel * dt
        self.movement_collider.position = self.entity.position
        self.movement_collider.approach(target_pos, True)
        self.entity.position = self.movement_collider.position

    def _handle_horizontal_movement(self, dt):
        vel = make_vector(self.velocity.x, 0)
        self.movement_collider.position = self.entity.position

        target = self.entity.position + vel * dt

        self.movement_collider.approach(target, True)
        self.entity.position = self.movement_collider.position

    def _on_hit(self, collision):
        if collision.hit_block:
            # we hit a block, but it could have been from above. Determine if block is left or right
            is_left = any(self.airborne_collider.test(self.movement_collider.position - make_vector(1, 0)))
            is_right = any(self.airborne_collider.test(self.movement_collider.position + make_vector(1, 0)))

            # only flip directions if it will improve situation
            if (is_left and self.velocity.x < 0.) or (is_right and self.velocity.x > 0.):
                self._reverse_direction = True
        elif collision.hit_collider is not None and collision.hit_collider.layer == Layer.Enemy:
            self._reverse_direction = True
