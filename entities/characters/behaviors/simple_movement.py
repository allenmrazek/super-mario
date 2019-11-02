from .behavior import Behavior
from .gravity_movement import GravityMovement
from util import make_vector, copy_vector
from ..parameters import CharacterParameters
from entities.collider import Collider
import constants


class SimpleMovement(Behavior):
    """Moves according to given velocity (leftwards), affected by gravity. Doesn't do anything by itself when it
    hits something"""
    def __init__(self, entity, collider_manager, parameters, movement_mask=constants.Block | constants.Enemy,
                 on_collision_callback=None):
        assert entity is not None
        assert collider_manager is not None
        assert parameters is not None

        super().__init__()

        self.entity = entity
        self.collider_manager = collider_manager
        self.on_collision = on_collision_callback

        self.horizontal_movement_collider = Collider.from_entity(entity, collider_manager, movement_mask)

        self.parameters = parameters  # type: CharacterParameters
        self.velocity = make_vector(0., 0.)
        self.vertical_movement = GravityMovement(entity, collider_manager, parameters)
        self.vertical_movement.airborne_collider.mask = movement_mask & constants.Block

        # allow other things to collide with our movement collider. Note they
        # must have a mask that hits Layer.Enemy to do this
        collider_manager.register(self.horizontal_movement_collider)

    def destroy(self):
        self.collider_manager.unregister(self.horizontal_movement_collider)

    @property
    def is_airborne(self):
        return self.vertical_movement.is_airborne

    @property
    def velocity(self):
        return self.entity.velocity or make_vector(0, 0)

    @velocity.setter
    def velocity(self, vel):
        self.entity.velocity = copy_vector(vel)

    def on_horizontal_collision(self, collision):
        pass

    def update(self, dt):
        self.vertical_movement.update(dt)
        self._handle_horizontal_movement(dt)

    def draw(self, screen, view_rect):
        self.vertical_movement.draw(screen, view_rect)

    def _handle_horizontal_movement(self, dt):
        vel = make_vector(self.velocity.x, 0)
        self.horizontal_movement_collider.position = self.entity.position

        target = self.entity.position + vel * dt

        collisions = self.horizontal_movement_collider.try_move(target, True)

        if collisions:
            for c in collisions:
                self.on_horizontal_collision(c)

                if self.on_collision:
                    self.on_collision(c)
        else:
            self.entity.position = self.horizontal_movement_collider.position
