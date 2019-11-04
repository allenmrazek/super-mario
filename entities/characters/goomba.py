from . import Enemy
from entities.characters.corpse import Corpse
from .level_entity import LevelEntity
from .parameters import CharacterParameters
from .behaviors import EnemyGroundMovement, Squashable, DamageMario
from .projectile import Projectile
from util import make_vector, mario_str_to_pixel_value_acceleration as mstpva
from util import mario_str_to_pixel_value_velocity as mstpvv
from util import get_aligned_foot_position, world_to_screen
from scoring import labels
import config

goomba_parameters = CharacterParameters(100, mstpvv('04800'), mstpva('00700'), 100, mstpvv('04200'))


class Goomba(Enemy):
    POINT_VALUE = 100

    def __init__(self, level):
        self.animation = level.asset_manager.character_atlas.load_animation("goomba")

        super().__init__(level, self.animation.get_rect())

        self.movement = EnemyGroundMovement(self, level.collider_manager, goomba_parameters)
        self.parameters = goomba_parameters
        self.squishy = Squashable(level, self, (3, 5), (10, 7), goomba_parameters.squash_bounce_velocity, self.squash,
                                  self._on_mario_invincible_collision)

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.movement.update(dt)
        self.squishy.update(dt)

        if not self.movement.is_airborne:
            self.animation.update(dt)  # only move legs if on the ground

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

        self.movement.draw(screen, view_rect)
        self.squishy.draw(screen, view_rect)

    def _on_mario_invincible_collision(self, collision):
        if self.level.mario.is_starman:
            self.die()

    def squash(self):
        # goomba got squashed by mario
        self.destroy()

        self.level.stats.score += Goomba.POINT_VALUE

        corpse = Corpse(self.level, self.level.asset_manager.character_atlas.load_static("goomba_squashed"),
                        Corpse.STATIONARY, 1.)
        corpse.position = get_aligned_foot_position(self.rect, corpse.rect)

        self.level.asset_manager.sounds['stomp'].play()
        self.level.entity_manager.register(corpse)

        from .floaty_points import FloatyPoints
        FloatyPoints.display(self.level, Goomba.POINT_VALUE, self)

    def die(self):
        # goomba was flat-out killed (starman mario, shell, fireball)
        self.destroy()
        self.level.stats.score += Goomba.POINT_VALUE

        # note the differerence: this corpse will actually fall off screen
        corpse = Corpse.create_ghost_corpse_from_entity(self, self.animation, self.level, 5., Corpse.STANDARD)
        corpse.position = get_aligned_foot_position(self.rect, corpse.rect)

        self.level.asset_manager.sounds['stomp'].play()

        self.level.entity_manager.register(corpse)

        from .floaty_points import FloatyPoints
        FloatyPoints.display(self.level, Goomba.POINT_VALUE, self)

    def destroy(self):
        super().destroy()
        self.level.entity_manager.unregister(self)
        self.movement.destroy()
        self.squishy.destroy()

    def create_preview(self):
        return self.animation.image.copy()

    
LevelEntity.create_generic_factory(Goomba)
