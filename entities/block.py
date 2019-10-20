from pygame.sprite import Rect
from entities.entity import Entity, Layer
from entities.collider import Collider
from tileset import TileSet


class Block(Entity):
    __slots__ = ['collider', 'position', 'idx', 'tileset']

    def __init__(self, position, tileset: TileSet, idx, cmanager):
        r = Rect(position[0], position[1], tileset.dimensions[0], tileset.dimensions[1])
        super().__init__(r)

        self.collider = Collider(self, cmanager, 0)
        cmanager.register(self.collider)

        self.position = position
        self.idx = idx
        self.tileset = tileset

    def update(self, dt):
        pass  # basic blocks don't do any thinking

    def draw(self, screen):
        self.tileset.draw(screen, self.idx, self.position)

    @property
    def collision_mask(self):
        return 0

    @property
    def layer(self):
        return Layer.Block
