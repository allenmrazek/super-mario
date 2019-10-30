from . import Enemy
from entities.characters.corpse import Corpse
from .level_entity import LevelEntity, MovementParameters
from .behaviors import SimpleMovement, Squashable, DamageMario
from util import make_vector, mario_str_to_pixel_value_acceleration as mstvpa
from util import mario_str_to_pixel_value_velocity as mstvpv
from util import get_corpse_position, world_to_screen
from scoring import labels
import config

# Goomba
goomba_parameters = MovementParameters.create(100, mstvpv('04800'), mstvpv('04000'), 100, mstvpa('00300'))


class Goomba(Enemy):
    def __init__(self, level, position):
        self.animation = level.asset_manager.character_atlas.load_animation("goomba")

        super().__init__(level, position, self.animation.get_rect())

        self.movement = SimpleMovement(self, level.collider_manager, goomba_parameters)
        self.parameters = goomba_parameters
        self.squishy = Squashable(level, self, (3, 5), (10, 7), mstvpv('04000'), self.die)

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

    def die(self):
        self.destroy()
        labels.Labels.points += 100

        corpse = Corpse(self.level, self.level.asset_manager.character_atlas.load_static("goomba_squashed"),
                        1., self.position)
        self.level.asset_manager.sounds['stomp'].play()

        corpse.position = get_corpse_position(self.rect, corpse.rect)

        self.level.entity_manager.register(corpse)

    def destroy(self):
        self.level.entity_manager.unregister(self)
        self.movement.destroy()
        self.squishy.destroy()

    def create_preview(self):
        return self.animation.image.copy()

    
def make_goomba(level, values):
    goomba = Goomba(level, make_vector(0, 0))

    if values is not None:
        goomba.deserialize(values)

    return goomba


LevelEntity.register_factory(Goomba, make_goomba)
