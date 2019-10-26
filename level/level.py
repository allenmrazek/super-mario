import copy
from entities.entity import Layer, EntityManager
from entities.collider import ColliderManager
from assets.map import Map
import config
from util import make_vector
from entities.mario import Mario
from event import PlayerInputHandler
from event.game_events import EventHandler


class Level(EventHandler):
    """A level is the highest-level object containing everything that makes up a level"""
    def __init__(self, assets):
        super().__init__()

        self.entity_manager = EntityManager.create_default()
        self.map = Map((20, 10), assets.tileset)
        self.collider_manager = ColliderManager(self.map)
        self.asset_manager = assets
        self.player_input = PlayerInputHandler()
        self.mario = Mario(self.player_input, assets.character_atlas, self.collider_manager)
        self.entity_manager.register(self.mario)
        self.mario.position = make_vector(config.screen_rect.centerx, 0)

    def add_entity(self, entity):
        self.entity_manager.register(entity)

    def update(self, dt):
        self.entity_manager.update(dt)

    def draw(self, screen):
        self.map.draw(screen, config.screen_rect)
        self.entity_manager.draw(screen)

    def handle_event(self, evt, game_events):
        self.player_input.handle_event(evt, game_events)

    @staticmethod
    def create_default(assets):
        lvl = Level(assets)

        return lvl
