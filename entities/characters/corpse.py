from ..entity import Entity, Layer
from util import world_to_screen


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
            self.level.entity_manager.unregister(self)

    @property
    def layer(self):
        return Layer.Enemy

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))
