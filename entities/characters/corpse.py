import pygame
from animation import StaticAnimation
from .projectile import Projectile
import constants
from util import get_aligned_foot_position
from .parameters import CharacterParameters
from util import make_vector
from util import mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva


class Corpse(Projectile):
    STATIONARY = CharacterParameters(0., 0., 0., 0., 0.)
    STANDARD = CharacterParameters(0., mstpvv('04200'), mstpva('00280'), mstpvv('04000'), mstpvv('04000'))

    """Stays on-screen for a while, then disappears."""

    def __init__(self, level, animation, parameters, duration, ignore_ground=False):
        super().__init__(animation, level, parameters, (0, 0), animation.rect.size, 0, 0)

        self.level = level
        self.duration = duration
        self.animation = animation

        # kind of kludgy, but we need to edit GravityMovement's colliders if the corpse
        # is to ignore the ground
        if ignore_ground:
            self.movement.vertical_movement.airborne_collider.mask = 0  # will always be "airborne"

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.duration -= dt

        if self.duration < 0.:
            self.destroy()

    @property
    def layer(self):
        return constants.Active

    def destroy(self):
        self.level.entity_manager.unregister(self)

    def on_movement_collision(self, collision):
        pass

    def on_hit(self, collision):
        pass

    @staticmethod
    def create_corpse_animation(animation):
        current_frame = animation.image

        corpse = pygame.transform.flip(current_frame, False, True)

        return StaticAnimation(corpse)

    @staticmethod
    def create_ghost_corpse_from_entity(entity, entity_animation, level, duration, parameters=STATIONARY, initial_y=0.):
        # creates a special type of corpse which is inverted and falls off the screen, ignoring blocks
        corpse_animation = Corpse.create_corpse_animation(entity_animation)

        corpse = Corpse(level, corpse_animation, parameters, duration, ignore_ground=True)
        corpse.position = get_aligned_foot_position(entity.rect, corpse.rect)

        corpse.movement.velocity = make_vector(0., initial_y or -parameters.jump_velocity)
        return corpse
