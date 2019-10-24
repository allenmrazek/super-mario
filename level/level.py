from entities.entity import Layer, EntityManager
from entities.collider import ColliderManager
from . import AssetManager
import config
from util import make_vector


class Level:
    def __init__(self, atlas):
        self.entity_manager = EntityManager.create_default()
        self.collider_manager = ColliderManager()
        self.asset_manager = AssetManager(atlas, self.collider_manager)

    def add_entity(self, entity):
        self.entity_manager.register(entity)

    def update(self, dt):
        self.entity_manager.update(dt)

    def draw(self, screen):
        self.entity_manager.draw(screen)

    @staticmethod
    def create_default(atlas):
        lvl = Level(atlas)

        # create background blocks
        for xpos in range(0, config.screen_rect.width, 16 * config.rescale_factor):
            block = lvl.asset_manager.load_test_block(lvl.collider_manager)
            block.position = make_vector(xpos, config.screen_rect.bottom - block.height)
            lvl.add_entity(block)

        return lvl
