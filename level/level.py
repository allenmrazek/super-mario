from entities.entity import Layer, EntityManager
from entities.collider import ColliderManager
from assets import AssetManager
import config
from util import make_vector
from entities.mario import Mario
from event import PlayerInputHandler
from event.game_events import EventHandler
from assets import TileMap, TileSet
from assets.load import load_solid_block_atlas, load_background_block_atlas


class Level(EventHandler):
    def __init__(self, assets):
        super().__init__()

        self.entity_manager = EntityManager.create_default()
        self.collider_manager = ColliderManager()
        self.asset_manager = assets
        self.player_input = PlayerInputHandler()
        self.mario = Mario(self.player_input, assets.character_atlas, self.collider_manager)
        self.entity_manager.register(self.mario)
        self.mario.position = make_vector(config.screen_rect.centerx, 0)
        #self.mario.position = make_vector(config.screen_rect.centerx, config.screen_rect.bottom - self.mario.height)
        #self.background_map = TileMap.create_random((200, 100), self.asset_manager.background_tileset)

        self.background_map = TileMap.create_from_example_image("images/editor/level_backgrounds/bg2-2-end.png",
                                                                TileSet(load_background_block_atlas(False)))
        self.background_map.tileset = self.asset_manager.background_tileset

        self.map = TileMap.create_from_example_image("images/editor/level_backgrounds/bg2-2-end.png",
                                                     TileSet(load_solid_block_atlas(False)))
        self.map.tileset = self.asset_manager.solid_tileset  # because the one the TM is using wasn't scaled


    def add_entity(self, entity):
        self.entity_manager.register(entity)

    def update(self, dt):
        self.entity_manager.update(dt)

    def draw(self, screen):
        self.background_map.draw(screen, config.screen_rect)
        self.map.draw(screen, config.screen_rect)
        self.entity_manager.draw(screen)

    def handle_event(self, evt, game_events):
        self.player_input.handle_event(evt, game_events)

    @staticmethod
    def create_default(assets):
        lvl = Level(assets)

        # fill background
        # ~240 FPS without background
        # usable framerate with background -> optimize later

        # ctr = 0
        #
        # bkg_block = lvl.asset_manager.load_test_background().animation
        #
        # num_across = config.screen_rect.width // bkg_block.width
        # num_down = config.screen_rect.height // bkg_block.height
        #
        # expected = num_across * num_down
        #
        # for xpos in range(0, config.screen_rect.width, bkg_block.width):
        #     for ypos in range(0, config.screen_rect.height, bkg_block.height):
        #         bkg = lvl.asset_manager.load_test_background()
        #         bkg.position = make_vector(xpos, ypos)
        #         lvl.add_entity(bkg)
        #         ctr += 1
        #
        # print("number of bkg drawables: ", ctr)

        # create solid blocks on floor
        # for xpos in range(-config.screen_rect.width, config.screen_rect.width * 2, 16 * config.rescale_factor):
        #     block = lvl.asset_manager.load_test_block(lvl.collider_manager)
        #     block.position = make_vector(xpos, config.screen_rect.bottom - block.height)
        #     lvl.add_entity(block)
        #
        # # create small solid layer 4 blocks high on left
        # for xpos in range(0, 16 * config.rescale_factor * 4, 16 * config.rescale_factor):
        #     block = lvl.asset_manager.load_test_block(lvl.collider_manager)
        #     block.position = make_vector(xpos, config.screen_rect.bottom - block.height * 5)
        #     lvl.add_entity(block)

        return lvl
