from ..entity import Entity
from util import world_to_screen
import constants


class Corpse(Entity):
    """Stays on-screen for a while, then disappears. not interactive"""
    def __init__(self, level, animation, duration, position):
        super().__init__(animation.rect)

        self.level = level
        self.duration = duration
        self.animation = animation
        self.position = position

    def update(self, dt, view_rect):
        self.animation.update(dt)

        self.duration -= dt

        if self.duration < 0.:
            self.destroy()

    @property
    def layer(self):
        return constants.Enemy

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

    def destroy(self):
        self.level.entity_manager.unregister(self)
