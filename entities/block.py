from entities.entity import Entity, DrawLayer
from entities.entity import CollisionLayer
from tileset import TileSet


class Block(Entity):
    def __init__(self, position, tileset: TileSet, idx):
        super().__init__()
        self.position = position
        self.idx = idx
        self.tileset = tileset

    def update(self, dt):
        pass  # basic blocks don't do any thinking

    def draw(self, screen):
        self.tileset.draw(screen, self.idx, self.position)

    def on_collision(self, other_entity):
        pass

    @property
    def collision_mask(self):
        return 0

    @property
    def layer(self):
        return DrawLayer.Block
