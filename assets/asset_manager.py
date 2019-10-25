import os
from entities import Block
from entities import Drawable
from util import make_vector
from assets import TileSet
from .sprite_atlas import SpriteAtlas
from .load import *
import config


class AssetManager:
    """AssetManager is the central location for all assets in the game"""
    def __init__(self):
        self.background_atlas = load_background_block_atlas()
        self.solid_atlas = load_solid_block_atlas()
        self.interactive_atlas = load_interactive_block_atlas()

        self.background_tileset = TileSet(self.background_atlas)
        self.solid_tileset = TileSet(self.solid_atlas)
        self.character_atlas = load_character_atlas()

        self.gui_atlas = load_gui_atlas()
        self.misc_atlas = load_misc_atlas()

