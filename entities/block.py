from pygame.sprite import Rect
from entities.entity import Entity, Layer
from entities.collider import Collider


class Block(Entity):
    def __init__(self, position, animation, cmanager):
        assert animation is not None

        r = Rect(position[0], position[1], animation.width, animation.height)
        super().__init__(r)

        self.collider = Collider.from_entity(self, cmanager, 0)
        self.position = position
        self.animation = animation

        cmanager.register(self.collider)

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

    # need to override position to propagate any changes to block's collider
    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, new_pos):
        super(Block, self.__class__).position.fset(self, new_pos)
        self.collider.position = new_pos
