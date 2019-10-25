from entities.entity import Layer, EntityManager
from entities.collider import ColliderManager
from assets import AssetManager
import config
from util import make_vector
from entities.mario import Mario
from event import PlayerInputHandler
from event.game_events import EventHandler


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

    def add_entity(self, entity):
        self.entity_manager.register(entity)

    def update(self, dt):
        self.entity_manager.update(dt)

    def draw(self, screen):
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
        for xpos in range(-config.screen_rect.width, config.screen_rect.width * 2, 16 * config.rescale_factor):
            block = lvl.asset_manager.load_test_block(lvl.collider_manager)
            block.position = make_vector(xpos, config.screen_rect.bottom - block.height)
            lvl.add_entity(block)

        # create small solid layer 4 blocks high on left
        for xpos in range(0, 16 * config.rescale_factor * 4, 16 * config.rescale_factor):
            block = lvl.asset_manager.load_test_block(lvl.collider_manager)
            block.position = make_vector(xpos, config.screen_rect.bottom - block.height * 5)
            lvl.add_entity(block)

        return lvl
