from entities import Block
from entities import Drawable
from util import make_vector


class AssetManager:
    """AssetManager creates instances of entities"""
    def __init__(self, atlas):
        assert atlas is not None

        self.atlas = atlas

    def load_test_block(self, collision_manager):
        return Block(make_vector(0, 0), self.atlas.load_static("misc_gray_bricks"), collision_manager)

    def load_test_background(self):
        return Drawable(make_vector(0, 0), self.atlas.load_static("green_square"))
