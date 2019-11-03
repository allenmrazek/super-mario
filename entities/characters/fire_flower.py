from ..entity import Entity
import constants
from util import world_to_screen


class FireFlower(Entity):
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

    @property
    def layer(self):
        return constants.Background
