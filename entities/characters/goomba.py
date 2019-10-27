from entities import Entity, Layer
from entities import Collider, ColliderManager
from .parameters import EnemyParameters
from .behaviors import SimpleMovement, JumpingMovement, HurtMario
from util import make_vector, mario_str_to_pixel_value_acceleration as mstvpa, mario_str_to_pixel_value_velocity as mstvpv
import config

# Goomba
goomba_parameters = EnemyParameters.create(100, mstvpv('04800'), mstvpv('04000'), 100, mstvpa('00300'))


class Goomba(Entity):
    def __init__(self, assets, collider_manager):
        self.animation = assets.character_atlas.load_animation("goomba")

        super().__init__(self.animation.get_rect())

        self.movement = SimpleMovement(self, collider_manager, goomba_parameters)
        self.parameters = goomba_parameters
        self.hurts = HurtMario(self, collider_manager, (3, 5), (10, 7))

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.movement.update(dt)
        self.hurts.update(dt)

        if not self.movement.is_airborne:
            self.animation.update(dt)  # only move legs if on the ground

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.animation.image, make_vector(*self.position) - make_vector(*view_rect.topleft))

        self.movement.draw(screen, view_rect)
        self.hurts.draw(screen, view_rect)

    @property
    def layer(self):
        return Layer.Enemy
