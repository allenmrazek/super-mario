from pygame.sprite import Rect
from entities.entity import Entity, Layer
from entities.collider import Collider


class Block(Entity):
    __slots__ = ['collider', 'position', 'idx']

    def __init__(self, position, animation, cmanager):
        assert animation is not None

        r = Rect(position[0], position[1], animation.width, animation.height)
        super().__init__(r)

        self.collider = Collider(self, cmanager, 0)
        cmanager.register(self.collider)

        self.position = position
        self.animation = animation

    def update(self, dt):
        pass  # basic blocks don't do any thinking

    def draw(self, screen):
        screen.blit(self.animation.image, self.position)

    @property
    def collision_mask(self):
        return 0

    @property
    def layer(self):
        return Layer.Block
