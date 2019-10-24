import os
from enum import Enum
import pygame
import config
from atlas.load import get_atlas_path


class Classification(Enum):
    Background = "atlas_background_blocks"
    SolidNoninteractive = "atlas_solid_blocks"
    SolidInteractive = "atlas_interactive_blocks"
    Pickup = "atlas_pickups"
    Ignore = "atlas_ignored_blocks"
    NotClassified = "unknown"


class TileNameGenerator:
    base_name = "_tile_"
    ext = ".png"

    def __init__(self, directory, classification):
        self.counter = 0
        self.directory = directory
        self.base_name = f'{classification.name}{TileNameGenerator.base_name}'

    @property
    def current_filename(self):
        counter_str = str(self.counter).rjust(3, '0')

        return os.path.join(self.directory, f'{self.base_name}{counter_str}{self.ext}')

    def __iter__(self):
        while self.counter < 10000:
            while os.path.exists(self.current_filename):
                self.counter += 1

            yield self.current_filename


class Tile:
    def __init__(self, surface, classification):
        self.surface = surface
        self.classification = classification

    @staticmethod
    def load_from_file(path, classification):
        """Load an already-extracted tile. Assumes transparent color (magenta) should be ignored in hash"""
        if not os.path.exists(path) or not os.path.isfile(path):
            raise FileNotFoundError

        surf = pygame.image.load(path).convert(24)

        return Tile(surf, classification)

    @staticmethod
    def create_from_surface(surface, rect, surf_transparent, classification):
        surf = surface.subsurface(rect)

        with pygame.PixelArray(surf) as pixels:
            # convert any world-transparent pixels to config transparent pixels (magenta)
            for y in range(rect.height):
                for x in range(rect.width):
                    clr = surf.unmap_rgb(pixels[x, y])

                    if clr == surf_transparent:
                        pixels[x, y] = surf.map_rgb(config.transparent_color)

            tile = Tile(surf, Classification.NotClassified)

            Tile._save_tile(tile, classification)

            return tile

    @staticmethod
    def _save_tile(tile, classification):
        if classification == Classification.NotClassified:
            return

        # generate a name for this tile based on its classification
        directory = os.path.join("../../images/", classification.value)

        filename = next(iter(TileNameGenerator(directory, classification)))

        pygame.image.save(tile.surface.convert(), filename)

