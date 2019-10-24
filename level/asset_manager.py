from entities.block import Block
from util import make_vector


class AssetManager:
    """AssetManager creates instances of entities"""
    def __init__(self, atlas):
        assert atlas is not None

        self.atlas = atlas

    def load_test_block(self, collision_manager):
        return Block(make_vector(0, 0), self.atlas.load_static("brown_square"), collision_manager)
