from .simple_movement import SimpleMovement


class JumpingMovement(SimpleMovement):
    """Jumps immediately whenever it hits the ground"""
    def __init__(self, entity, collider_manager, parameters, movement_collider=None):
        super().__init__(entity, collider_manager, parameters, movement_collider)

    def update(self, dt):
        super().update(dt)

        if not self.is_airborne:
            self.velocity.y = -self.parameters.jump_velocity
