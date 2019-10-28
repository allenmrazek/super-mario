from pygame import Rect
from entities.entity_manager import EntityManager
from entities.collider import ColliderManager
from assets.tile_map import TileMap
import config
from util import make_vector, copy_vector
from entities.characters import Mario, MarioSpawnPoint
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
        self.filename = "test_level.lvl"

        self.asset_manager = assets
        self.player_input = PlayerInputHandler()
        self.mario = Mario(self.player_input, self)

        self._scroll_position = make_vector(0, 0)
        self._view_rect = Rect(0, 0, config.screen_rect.width, config.screen_rect.height)

    def add_entity(self, entity):
        self.entity_manager.register(entity)

    def update(self, dt):
        self.entity_manager.update(dt, self.view_rect)

    def draw(self, screen):
        vr = self.view_rect  # send copy: don't want our private stuff messed with

        self.tile_map.draw(screen, vr)
        self.entity_manager.draw(screen, vr)

    def handle_event(self, evt, game_events):
        self.player_input.handle_event(evt, game_events)

    def spawn_mario(self, spawn_point):
        assert spawn_point is not None and isinstance(spawn_point, MarioSpawnPoint)

        # todo: avoid double spawn?
        self.entity_manager.register(self.mario)
        self.mario.enabled = True
        assert self.mario.enabled

        self.mario.reset()
        self.mario.position = make_vector(config.screen_rect.centerx, 33)

    def despawn_mario(self):
        print("despawning mario")

        assert self.mario.enabled

        # mario handles his own registration
        self.mario.enabled = False

    def serialize(self):
        return {"name": "unknown",
                "filename": self.filename,
                "background_color": self.background_color,
                "tile_map": self.tile_map.serialize(),
                "entities": self.entity_manager.serialize()}

    def deserialize(self, values):
        if self.mario.enabled:
            self.despawn_mario()

        self.filename = values["filename"]
        self.background_color = tuple(values["background_color"])
        self.tile_map.deserialize(values["tile_map"])
        self.entity_manager.deserialize(self, values["entities"])

        # search for mario spawn point(s)
        spawn_points = self.entity_manager.search_by_type(MarioSpawnPoint)

        # order spawn points by x location
        spawn_points.sort(key=lambda left, right: left[0] < right[0])

        # todo: checkpoints?

        if spawn_points:
            self.spawn_mario(spawn_points[0])


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
