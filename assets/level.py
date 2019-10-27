import copy
from pygame import Rect
from entities.entity import Layer, EntityManager
from entities.collider import ColliderManager
from assets.tile_map import TileMap
import config
from util import make_vector, copy_vector
from entities.mario import Mario
from event import PlayerInputHandler
from event.game_events import EventHandler
from entities.characters import Goomba


class Level(EventHandler):
    """A level is the highest-level object containing everything that makes up a level"""
    def __init__(self, assets):
        super().__init__()

        self.entity_manager = EntityManager.create_default()
        self.tile_map = TileMap((30, 20), assets.tileset)
        self.collider_manager = ColliderManager(self.tile_map)
        self.background_color = (0, 0, 0)

        self.asset_manager = assets
        self.player_input = PlayerInputHandler()
        self.mario = Mario(self.player_input, assets.character_atlas, self.collider_manager)
        self.entity_manager.register(self.mario)
        self.mario.position = make_vector(config.screen_rect.centerx, 33)

        self.goomba = Goomba(assets, self.collider_manager)
        self.goomba.position = make_vector(config.screen_rect.centerx + 60, 33)
        self.entity_manager.register(self.goomba)

        self._scroll_position = make_vector(0, 0)
        self._view_rect = Rect(0, 0, config.screen_rect.width, config.screen_rect.height)

    def add_entity(self, entity):
        self.entity_manager.register(entity)

    def update(self, dt):
        self.entity_manager.update(dt, self.view_rect)

    def draw(self, screen):
        vr = self.view_rect # send copy: don't want our private stuff messed with

        self.tile_map.draw(screen, vr)
        self.entity_manager.draw(screen, vr)

    def handle_event(self, evt, game_events):
        self.player_input.handle_event(evt, game_events)

    @property
    def view_rect(self):
        return self._view_rect.copy()

    @property
    def position(self):
        return copy_vector(self._scroll_position)

    @position.setter
    def position(self, new_pos):
        self._scroll_position = make_vector(new_pos[0], new_pos[1])
        self._view_rect.topleft = self._scroll_position

    @staticmethod
    def create_default(assets):
        lvl = Level(assets)

        return lvl
