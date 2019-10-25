import os
import itertools

import pygame
from entities.gui.drawing import smart_draw
import config
from tools.TileExtractor.tile_identifier import is_exact_match_to_anchor
from animation import Animation


class TileSet:
    """ note to self: rather than having hundreds of background/foreground tiles, instead they'll all exist in
    this TileSet. The tileset as a whole will be updated (allowing for animation backgrounded/solid tiles)"""
    def __init__(self, tile_atlas):
        # self.library = TileSet.load_library(library_path)
        #
        # self.warn_on_missing(tile_atlas, self.library)

        # for now, use simple indices

        self.atlas = tile_atlas
        self.tiles = []

        for _, animation in itertools.chain(tile_atlas.animations.items(), tile_atlas.statics.items()):
            self.tiles.append(animation)

        self.tile_width = 8 * config.rescale_factor
        self.tile_height = 8 * config.rescale_factor

    # # using the library
    # @staticmethod
    # def load_library(path):
    #     if not os.path.exists(path):
    #         raise FileNotFoundError
    #
    #     # library format: { file_name: int, ... }
    #     # disk format:
    #     # filename, index
    #
    #     library = {}
    #
    #     with open(path) as f:
    #         indices = set()
    #
    #         for line in f:
    #             entry = line.split(',')
    #
    #             if len(entry) != 2:
    #                 print(f"Warning: line '{line}' is invalid")
    #
    #             if entry[0] in library:
    #                 print(f"Warning: {entry[0]} is a duplicate")
    #
    #             idx = int(entry[1])
    #
    #             if idx in indices:
    #                 print(f"*** warning *** a tile with index {idx} already exists in the library!")
    #
    #             library[entry[0]] = idx
    #
    #     return library
    #
    # @staticmethod
    # def save_library(path):
    #     pass
    #
    # @staticmethod
    # def warn_on_missing(atlas, library):
    #     existing = set(atlas.sprite_names)
    #     library_file_names = set([x[0] for x in library])
    #
    #     missing = library_file_names.difference(existing)
    #
    #     if missing:
    #         print(f"Warn! Missing {len(missing)} tiles from tile set")
    #
    #         for m in missing:
    #             print(f"  missing: {m}")

    def draw(self, screen, pos, idx):
        assert 0 <= idx <= len(self.tiles)

        screen.blit(self.tiles[idx].image, pos)

    def find_match(self, other_surface, other_pixels, other_rect, other_trans_color):
        other_trans_color = other_trans_color or config.transparent_color

        for i, _ in enumerate(self.tiles):
            if self.is_exact_match(i, other_surface, other_pixels, other_rect, other_trans_color):
                return i

        return None

    def is_exact_match(self, idx, other, other_pixels, other_rect, other_trans_color):
        for frame in self.tiles[idx].frames:
            if is_exact_match_to_anchor(frame, other, other_pixels, other_rect,
                                        other_trans_color):
                return True

        return False
