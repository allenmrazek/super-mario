from .tileset import TileSet
from .load import *


class AssetManager:
    """AssetManager is the central location for all assets in the game"""
    def __init__(self):
        self.tileset = TileSet("images/tiles.png")
        self.character_atlas = load_character_atlas()
        self.pickup_atlas = load_pickup_atlas()

        self.gui_atlas = load_gui_atlas()
        self.misc_atlas = load_misc_atlas()

