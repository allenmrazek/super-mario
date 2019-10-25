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

        self.tile_width, self.tile_height = config.base_tile_dimensions[0] * config.rescale_factor, \
                                            config.base_tile_dimensions[1] * config.rescale_factor

        src_rect = pygame.Rect(0, 0, self.tile_width, self.tile_height)

        for x in range(0, self.surface.get_width(), self.tile_width):
            for y in range(0, self.surface.get_height(), self.tile_height):
                src_rect.x, src_rect.y = x + x // self.tile_width * config.rescale_factor,\
                                         y + y // self.tile_height * config.rescale_factor

                if src_rect.right >= self.surface.get_width() or src_rect.bottom >= self.surface.get_height():
                    continue

                self.tiles.append(self.surface.subsurface(src_rect))

        self.tile_count = len(self.tiles)

    def blit(self, screen, pos, idx):
        assert 0 <= idx < self.tile_count

        screen.blit(self.tiles[idx], pos)
