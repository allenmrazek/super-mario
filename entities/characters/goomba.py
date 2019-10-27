from . import Enemy
from entities.characters.corpse import Corpse
from .parameters import EnemyParameters
from .behaviors import SimpleMovement, Squashable
from util import make_vector, mario_str_to_pixel_value_acceleration as mstvpa
from util import mario_str_to_pixel_value_velocity as mstvpv
from util import get_corpse_position
import config

# Goomba
goomba_parameters = EnemyParameters.create(100, mstvpv('04800'), mstvpv('04000'), 100, mstvpa('00300'))


class Goomba(Enemy):
    def __init__(self, level, position):
        self.animation = level.asset_manager.character_atlas.load_animation("goomba")

        super().__init__(level, position, self.animation.get_rect())

        self.movement = SimpleMovement(self, level.collider_manager, goomba_parameters)
        self.parameters = goomba_parameters
        self.hurts = Squashable(level, self, (3, 5), (10, 7), mstvpv('04000'), self.die)

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

    def die(self):
        print("goomba died")

        self.level.entity_manager.unregister(self)
        self.movement.finish()

        corpse = Corpse(self.level, self.level.asset_manager.character_atlas.load_static("goomba_squashed"),
                        1., self.position)

        corpse.position = get_corpse_position(self.rect, corpse.rect)

        self.level.entity_manager.register(corpse)
