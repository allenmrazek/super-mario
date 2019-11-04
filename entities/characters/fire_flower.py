from ..entity import Entity
import constants
from util import world_to_screen
from .floaty_points import FloatyPoints


class FireFlower(Entity):
    POINT_VALUE = 1000

    def __init__(self, level, position):
        self.animation = level.asset_manager.pickup_atlas.load_animation("fire_flower")

        super().__init__(self.animation.get_rect())

        from .behaviors import Interactive

        self.collect = Interactive(level, self, (2, 0), (12, 14), self.on_collected)
        self.level = level
        self.position = position

    def update(self, dt, view_rect):
        self.animation.update(dt)
        self.collect.update(dt)

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))
        self.collect.draw(screen, view_rect)

    def on_collected(self, collision):
        self.level.asset_manager.sounds['powerup'].play()
        self.level.entity_manager.unregister(self)

        mario = self.level.mario

        if not mario.is_super:
            from ..effects.mario_transform_super import MarioTransformSuper

            MarioTransformSuper.apply_transform(self.level, mario)
        else:
            from .mario.mario import MarioEffectFire
            mario.effects |= MarioEffectFire

        FloatyPoints.display(self.level, FireFlower.POINT_VALUE, self)

    @property
    def layer(self):
        return constants.Background
