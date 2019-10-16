import os
import pygame
from typing import NamedTuple
import config


class _Tile(NamedTuple):
    surface: pygame.Surface
    rect: pygame.Rect


class TileSet:
    def __init__(self, image_path, tile_dimensions, color_key=None):
        path = os.fsencode(os.path.join("images", os.path.join("tilesets", image_path)))

        if not os.path.exists(path) or not os.path.isfile(path):
            raise FileNotFoundError

        # load image
        try:
            self.map = pygame.image.load(os.fsdecode(path))
        except pygame.error:
            print("Error reading %s: %s" % (image_path, pygame.get_error()))
            raise

        # Scale image, if needed
        w, h = self.map.get_width() * config.rescale_factor, self.map.get_height() * config.rescale_factor
        tile_dimensions *= config.rescale_factor

        self.map = pygame.transform.scale(self.map, (w, h)).convert()  # avoids per-pixel alpha, if any

        if color_key is not None:
            self.map.set_colorkey(color_key)

        # split into tiles
        self.tiles = []
        x_tiles, y_tiles = w // tile_dimensions[0], h // tile_dimensions[1]

        for y in range(y_tiles):
            for x in range(x_tiles):
                rect = pygame.Rect(x * tile_dimensions[0], y * tile_dimensions[1], tile_dimensions[0], tile_dimensions[1])
                tile = self.map.subsurface(rect)

                self.tiles.append(_Tile(tile, rect))

        self._draw_rect = pygame.Rect(0, 0, tile_dimensions[0], tile_dimensions[1])
        self.dimensions = (tile_dimensions, tile_dimensions)

    def draw(self, screen, tile_idx, tile_position):
        if tile_idx is None:
            return

        self._draw_rect.x, self._draw_rect.y = int(tile_position[0]), int(tile_position[1])

        screen.blit(self.tiles[tile_idx].surface, self._draw_rect)

    @property
    def num_tiles(self):
        return (self.map.get_width() // self.dimensions[0]) * (self.map.get_height() // self.dimensions[1])
