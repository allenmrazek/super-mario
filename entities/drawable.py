from .entity import Entity
from pygame import Rect


class Drawable(Entity):
    def __init__(self, position, animation):
        assert animation is not None

        r = Rect(position[0], position[1], animation.width, animation.height)
        super().__init__(r)

        self.position = position
        self.animation = animation

    def draw(self, screen):
        screen.blit(self.animation.image, self.position)

    def update(self, dt):
        pass
