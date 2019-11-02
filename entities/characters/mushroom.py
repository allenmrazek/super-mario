from entities.entity import Entity
import entities.characters.behaviors
from .parameters import CharacterParameters
from util import world_to_screen, mario_str_to_pixel_value_acceleration as mstpva, \
    mario_str_to_pixel_value_velocity as mstpvv
import entities.effects
import constants


# todo: scale this by rescale factor?
mushroom_movement = CharacterParameters(50, mstpvv('04000'), 0., 0., mstpva('00300'))


class Mushroom(Entity):
    POINT_VALUE = 1000

    def __init__(self, level, position):
        self.animation = level.asset_manager.pickup_atlas.load_static("mushroom_red")

        super().__init__(self.animation.image.get_rect())

        self.level = level
        self.pickup = entities.characters.behaviors.interactive.Interactive(
            level, self, (0, 0), (16, 16), self.on_collected)
        self.movement = entities.characters.behaviors.simple_movement.SimpleMovement(
            self, level.collider_manager, mushroom_movement)
        self.movement.horizontal_movement_collider.mask = constants.Block  # exclude enemies

        self.position = position

    def update(self, dt, view_rect):
        self.movement.update(dt)
        self.pickup.update(dt)

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

        self.movement.draw(screen, view_rect)
        self.pickup.draw(screen, view_rect)

    def on_collected(self, collision):
        self.level.entity_manager.unregister(self)
        self.level.stats.score += Mushroom.POINT_VALUE

        entities.effects.mario_transform_super.MarioTransformSuper.apply_transform(self.level, self.level.mario)
