from entities.block import Block
from util import make_vector


class AssetManager:
    """AssetManager creates instances of entities"""
    def __init__(self, atlas, collision_manager):
        assert atlas is not None
        assert collision_manager is not None

        self.atlas = atlas
        self.collision_manager = collision_manager

    def load_test_block(self, collision_manager):
        return Block(make_vector(0, 0), self.atlas.load_static("tile_013"), cmanager=self.collision_manager)
