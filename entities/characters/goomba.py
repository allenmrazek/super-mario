from entities import Entity, Layer
from entities import Collider, ColliderManager
from .parameters import EnemyParameters
from .behaviors import SimpleMovement
from util import make_vector, mario_str_to_pixel_value_acceleration as mstvpa, mario_str_to_pixel_value_velocity as mstvpv
import config

# Goomba
goomba_parameters = EnemyParameters.create(100, mstvpv('04800'), 100, 100, mstvpa('00600'))


class Goomba(Entity):
    def __init__(self, assets, collider_manager):
        self.animation = assets.character_atlas.load_animation("goomba")

        super().__init__(self.animation.get_rect())

        self.movement = SimpleMovement(self, collider_manager, goomba_parameters)
        self.parameters = goomba_parameters

        self.hitbox = Collider.from_entity(self, collider_manager, Layer.Mario)
        self.hitbox.rect.width = 10 * config.rescale_factor
        self.hitbox.rect.height = 7 * config.rescale_factor

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.movement.update(dt)

        if not self.movement.is_airborne:
            self.animation.update(dt)  # only move legs if on the ground

        self.hitbox.position = self.position + make_vector(3 * config.rescale_factor, 5 * config.rescale_factor)

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.animation.image, make_vector(*self.position) - make_vector(*view_rect.topleft))

        if config.debug_hitboxes:
            screen.fill((0, 255, 0), self.hitbox.rect)



    @property
    def layer(self):
        return Layer.Enemy
