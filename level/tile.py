import os
from enum import Enum
import pygame
import config
from . import calc_hash


class Classification(Enum):
    Background = "atlas_background_blocks"
    SolidNoninteractive = "atlas_solid_blocks"
    SolidInteractive = "atlas_interactive_blocks"
    NotClassified = "unknown"


class Tile:
    def __init__(self, surface, hashcode, classification):
        self.surface = surface
        self.hashcode = hashcode
        self.classication = classification

        print("created tile with hashcode ", hashcode)

    @staticmethod
    def load_from_file(path, classification):
        """Load an already-extracted tile. Assumes transparent color (magenta) should be ignored in hash"""
        if not os.path.exists(path) or not os.path.isfile(path):
            raise FileNotFoundError

        surf = pygame.image.load(path).convert(32)

        with pygame.PixelArray(surf) as pixels:
            hashcode = calc_hash(surf, pixels, surf.get_rect(), config.transparent_color)
            return Tile(surf, hashcode[0], classification)

    @staticmethod
    def create_from_surface(surface, rect, surf_transparent):
        surf = surface.subsurface(rect)

        with pygame.PixelArray(surf) as pixels:
            # convert any world-transparent pixels to config transparent pixels (magenta)
            for y in range(rect.height):
                for x in range(rect.width):
                    clr = surf.unmap_rgb(pixels[x, y])

                    if clr == surf_transparent:
                        pixels[x, y] = surf.map_rgb(config.transparent_color)

            hashcode = calc_hash(surf, pixels, surf.get_rect(), config.transparent_color)
            return Tile(surf, hashcode[0], Classification.NotClassified)
