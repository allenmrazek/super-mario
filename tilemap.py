import os
from tileset import TileSet
from entities.entity import Entity


class Block(Entity):
    def __init__(self, position, idx, collides):
        super().__init__()
        self.position = position
        self.idx = idx
        self.collides = collides

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def collision_mask(self):
        pass


class TileMap:
    def __init__(self, tile_set: TileSet, size):
        self.tile_set = tile_set
        self.map = []
        self.width, self.height = size[0], size[1]

        for _ in range(self.width):
            self.map.append([None for _ in range(self.height)])

    @staticmethod
    def load_from_file(filename):
        fn = os.fsencode(filename)

        if not os.path.exists(fn) or not os.path.isfile(fn):
            raise FileNotFoundError

        raise NotImplementedError  # todo: file format

    def save_to_file(self, filename):
        raise NotImplementedError

    def draw(self, screen, view_region):
        # avoid drawing entire map by determining the subset of tiles visible in the given region
        x_min = int(view_region.left) // self.tile_set.dimensions[0]
        x_max = int(view_region.right) // self.tile_set.dimensions[0] + 1
        y_min = int(view_region.top) // self.tile_set.dimensions[1]
        y_max = int(view_region.bottom) // self.tile_set.dimensions[1] + 1

        tile_w, tile_h = self.tile_set.dimensions

        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                tile_idx = self.map[x][y]

                self.tile_set.draw(screen, tile_idx, (x * tile_w, y * tile_h))

    def set_tile(self, position, index=None):
        assert 0 <= position[0] <= self.width
        assert 0 <= position[1] <= self.height

        self.map[position[0]][position[1]] = index

