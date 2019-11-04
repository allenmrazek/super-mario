from ..entity import Entity
import constants
from util import world_to_screen
from .parameters import CharacterParameters
from util import mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from util import make_vector

starman_parameters = CharacterParameters(mstpvv('00750'), mstpvv('04000'), mstpva('00200'), mstpvv('02500'), 0.)


class Starman(Entity):
    DURATION = 15.

    def __init__(self, level, position):
        self.animation = level.asset_manager.pickup_atlas.load_animation("star")

        super().__init__(self.animation.get_rect())

        from .behaviors import Interactive
        from .behaviors import JumpingMovement

        self.collect = Interactive(level, self, (4, 4), (9, 9), self.on_collected)
        self.level = level
        self.position = position
        self.movement = JumpingMovement(self, level.collider_manager, starman_parameters, constants.Block)
        self.movement.velocity = make_vector(-starman_parameters.max_horizontal_velocity, 0.)

    def update(self, dt, view_rect):
        self.movement.update(dt)
        self.animation.update(dt)
        self.collect.update(dt)

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))
        self.collect.draw(screen, view_rect)

    def on_collected(self, collision):
        self.level.asset_manager.sounds['powerup'].play()
        self.level.entity_manager.unregister(self)

        mario = self.level.mario
        mario.make_starman(Starman.DURATION)

    def destroy(self):
        self.movement.destroy()

    @property
    def layer(self):
        return constants.Background
