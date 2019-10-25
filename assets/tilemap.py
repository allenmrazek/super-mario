import os
import random
import pygame
from . import TileSet
from tools.TileExtractor.tile_identifier import TileIdentifier, is_exact_match_to_anchor
import config


class TileMap:
    def __init__(self, map_size, tileset):
        self.map = []
        self.tileset = tileset
        self.width, self.height = map_size

        for _ in range(self.width):
            self.map.append([None for _ in range(self.height)])

    @staticmethod
    def load_from_file(filename):
        fn = os.fsencode(filename)

        if not os.path.exists(fn) or not os.path.isfile(fn):
            raise FileNotFoundError

        raise NotImplementedError  # todo: file format

    @staticmethod
    def create_random(size, tileset):
        tm = TileMap(size, tileset)

        for x in range(0, tm.width):
            for y in range(0, tm.height):
                tm.set_tile((x, y), random.randint(0, len(tileset.tiles) - 1))

        return tm

    def save_to_file(self, filename):
        raise NotImplementedError

    def draw(self, screen, view_region):
        # avoid drawing entire map by determining the subset of tiles visible in the given region
        tw, th = self.tileset.tile_width, self.tileset.tile_height

        x_min = int(view_region.left) // tw
        x_max = min(int(view_region.right) // tw + 1, self.width)
        y_min = int(view_region.top) // th
        y_max = min(int(view_region.bottom) // th + 1, self.height)

        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                try:
                    tile_idx = self.map[x][y]

                    if tile_idx is not None:
                        self.tileset.draw(screen, (x * tw, y * th), tile_idx)
                except IndexError:
                    print("")

    def set_tile(self, tile_position, index=None):
        assert 0 <= tile_position[0] <= self.width
        assert 0 <= tile_position[1] <= self.height

        self.map[tile_position[0]][tile_position[1]] = index

    @staticmethod
    def create_from_example_image(path, tileset_to_use: TileSet):
        """Lazy method to begin with a useful tilemap: just scan existing image to try and identify tiles. This will
        not get all tiles (entities might be covering some, some are actually entities, etc) but this will eliminate
        a lot of hand-editing"""
        if not os.path.exists(path):
            raise FileNotFoundError

        example_surface = pygame.image.load(path).convert()
        surface_rect = example_surface.get_rect()
        world_trans_color = example_surface.get_at((0, 0))

        # find anchor point to align grid
        anchor = TileIdentifier.find_anchor(example_surface, None, world_trans_color)

        if anchor is None:
            print("ERROR: couldn't find anchor in example image")
            raise RuntimeError

        tw, th = config.base_tile_dimensions
        tm = TileMap((surface_rect.width // tw, surface_rect.height // th), tileset_to_use)

        offset_x = anchor[0] % tw
        offset_y = anchor[1] % th

        start_x, start_y = offset_x, offset_y
        end_x = surface_rect.width
        end_y = surface_rect.height
        search_rect = pygame.Rect(0, 0, *config.base_tile_dimensions)
        found_counter = 0

        with pygame.PixelArray(example_surface) as example_pixels:
            for y in range(start_y, end_y, tw):
                for x in range(start_x, end_x, th):
                    search_rect.x, search_rect.y = x, y

                    if search_rect.right >= surface_rect.right or search_rect.bottom >= surface_rect.bottom:
                        continue  # can't possibly match enough pixels now

                    # try to match a tile
                    match = tileset_to_use.find_match(example_surface, example_pixels, search_rect, world_trans_color)

                    if match is not None:
                        tx, ty = (x - offset_x) // tw, (y - offset_y) // th
                        tm.set_tile((tx, ty), match)
                        found_counter += 1
                        print("matched ", found_counter, " tiles so far")

                print("x = ", x, "y = ", y)

        print(f"Successfully created {found_counter} tiles from example {path}")

        return tm
