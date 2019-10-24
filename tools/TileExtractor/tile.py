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
        """Load an already-extracted tile. Assumes transparent color (magenta) should be ignored in hash
        Note that one file may technically contain 'multiple' tiles if the tile is actually an animation """
        if not os.path.exists(path) or not os.path.isfile(path):
            raise FileNotFoundError

        surf = pygame.image.load(path).convert(24)

        return [Tile.create_from_surface(surf, pygame.Rect(x, 0, *config.base_tile_dimensions),
                                         config.transparent_color, classification, tf_save=False)
                for x in range(0, surf.get_width(), config.base_tile_dimensions[0])]

    @staticmethod
    def create_from_surface(surface, rect, surf_transparent, classification, tf_save=True):
        # remember: rect might have multiple tiles. Most of the time it doesn't, but convenient to handle the
        # situation here where it will be invisible to tile extractor
        surf = surface.subsurface(rect).convert(24)
        surf.set_alpha(None)

        with pygame.PixelArray(surf) as pixels:
            # convert any world-transparent pixels to config transparent pixels (magenta)
            for y in range(rect.height):
                for x in range(rect.width):
                    clr = surf.unmap_rgb(pixels[x, y])

                    if clr == surf_transparent:
                        pixels[x, y] = surf.map_rgb(config.transparent_color)
                    else:
                        pixels[x, y] = surf.map_rgb(clr.r, clr.g, clr.b)

            tile = Tile(surf, Classification.NotClassified)

            if tf_save:
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
