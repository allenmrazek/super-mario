import os
import pygame
from entities.gui.drawing import smart_draw


class TileSet:
    """A tileSet is:
    1) a collection of Animations (usually StaticAnimations) from an atlas
    2) the collection is indexed
    3) a library which maps tile name -> an index, to prevent changes in
       tile order from breaking anything that uses the tile set"""
    def __init__(self, tile_atlas, library_path):
        self.library = TileSet.load_library(library_path)

        self.warn_on_missing(tile_atlas, self.library)

    @staticmethod
    def load_library(path):
        if not os.path.exists(path):
            raise FileNotFoundError

        # library format: { file_name: int, ... }
        # disk format:
        # filename, index

        library = {}

        with open(path) as f:
            for line in f:
                entry = line.split(',')

                if len(entry) != 2:
                    print(f"Warning: line '{line}' is invalid")

                if entry[0] in library:
                    print(f"Warning: {entry[0]} is a duplicate")

                idx = int(entry[1])

                library[entry[0]] = idx

        return library

    @staticmethod
    def save_library(path):
        pass

    @staticmethod
    def warn_on_missing(atlas, library):
        existing = set(atlas.sprite_names)
        library_file_names = set([x[0] for x in library])

        missing = library_file_names.difference(existing)

        if missing:
            print(f"Warn! Missing {len(missing)} tiles from tile set")

            for m in missing:
                print(f"  missing: {m}")

    def draw(self, screen, pos, idx):
        pass
