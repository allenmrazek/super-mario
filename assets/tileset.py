import os
import pygame
import config


class TileSet:
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError

        self.path = path

        self.surface = pygame.image.load(path)
        self.surface = pygame.transform.scale(self.surface,
                                              (self.surface.get_width() * config.rescale_factor,
                                               self.surface.get_height() * config.rescale_factor))\
            .convert(pygame.display.get_surface())

        self.surface.set_colorkey(config.transparent_color)

        self.tiles = []

        self._tile_width, self._tile_height = config.base_tile_dimensions[0] * config.rescale_factor, \
            config.base_tile_dimensions[1] * config.rescale_factor

        src_rect = pygame.Rect(0, 0, self.tile_width, self.tile_height)

        self._across = 0
        self._down = 0

        for y in range(0, self.surface.get_height(), self.tile_height):
            row_counter = 0

            for x in range(0, self.surface.get_width(), self.tile_width):
                src_rect.x, src_rect.y = x + x // self.tile_width * config.rescale_factor,\
                                         y + y // self.tile_height * config.rescale_factor

                if src_rect.right >= self.surface.get_width() or src_rect.bottom >= self.surface.get_height():
                    continue

                self.tiles.append(self.surface.subsurface(src_rect))
                row_counter += 1

            self._across = max(self._across, row_counter)
            self._down += 1

        self.tile_count = len(self.tiles)

    def blit(self, screen, pos, idx):
        assert 0 <= idx < self.tile_count

        screen.blit(self.tiles[idx], pos)

    @property
    def tile_width(self):
        return self._tile_width

    @property
    def tile_height(self):
        return self._tile_height

    @property
    def tile_size(self):
        return self._tile_width, self.tile_height

    @property
    def num_tiles_per_row(self):
        return self._across

    @property
    def num_tiles_per_col(self):
        return self._down
