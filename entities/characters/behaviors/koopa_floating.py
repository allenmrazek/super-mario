import math
from .behavior import Behavior
from .squashable import Squashable
from ...collider import Collider
import constants
from util import make_vector, world_to_screen, copy_vector
import config


class KoopaFloating(Squashable):
    """This behavior moves the Koopa up and down vertically continuously. No horizontal motion """
    def __init__(self, level, entity, flight_range, hover_frequency, position,
                 bounce_velocity, on_squashed_callback, on_mario_invincible_callback):

        super().__init__(level, entity, (1, 10), (12, 12), bounce_velocity,
                         on_squashed_callback, on_mario_invincible_callback)

        self.level = level

        # create collider to avoid phasing through ground, blocks, or other enemies
        self.collider = Collider.from_entity(entity, level.collider_manager, constants.Block | constants.Enemy)
        level.collider_manager.register(self.collider)

        self.flight_range = flight_range
        self.b = 2 * math.pi * hover_frequency
        self.center_position = position
        self.elapsed = 0.
        self.velocity = make_vector(0, 0)

    def update(self, dt):
        pos = self.entity.position
        self.elapsed += dt

        pos.y = self.center_position.y + self.flight_range * math.cos(self.b * self.elapsed)
        self.collider.position = pos
        self.entity.position = pos
        self.velocity = make_vector(0, -math.sin(self.b * self.elapsed))

    def draw(self, screen, view_rect):
        if config.debug_hitboxes:
            r = self.collider.rect.copy()
            self.collider.position = self.entity.position
            r.topleft = world_to_screen(self.collider.position, view_rect)
            r = screen.get_rect().clip(r)
            screen.fill((0, 255, 0), r)

    def destroy(self):
        self.level.collider_manager.unregister(self.collider)

    @property
    def is_airborne(self):
        return True
