from pygame import Rect
from entities.collider import ColliderManager
from assets.tile_map import TileMap
import config
from util import make_vector, copy_vector
from entities.characters import Mario, MarioSpawnPoint
from event import PlayerInputHandler
from event.game_events import EventHandler


class Level(EventHandler):
    UPDATE_RECT_DISTANCE_FACTOR = 1.25  # entities within view_rect +- this factor * its width will be updated, else they'll be frozen

    """A level is the highest-level object containing everything that makes up a level"""
    def __init__(self, assets, entity_manager):
        super().__init__()

        assert entity_manager is not None
        assert assets is not None

        self.entity_manager = entity_manager
        self.tile_map = TileMap((60, 20), assets.tileset)
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

        # scroll map with mario
        if self.mario.enabled:
            left = self.mario.position.x - self.view_rect.width // 4

            self.position = make_vector(left if self.position.x < left else self.position.x, 0)

    def draw(self, screen):
        vr = self.view_rect  # send copy: don't want our private stuff messed with

        self.tile_map.draw(screen, vr)
        self.entity_manager.draw(screen, vr)

    def handle_event(self, evt, game_events):
        self.player_input.handle_event(evt, game_events)

    def spawn_mario(self, spawn_point=None):
        spawn_point = spawn_point or self._find_spawn_point()

        assert isinstance(spawn_point, MarioSpawnPoint)

        # todo: avoid double spawn?
        self.entity_manager.register(self.mario)
        self.mario.enabled = True
        assert self.mario.enabled

        self.mario.reset()
        self.mario.position = spawn_point.position

        # set level scroll position to be one quarter-screen behind mario, unless that would result in left edge
        # of map being visible
        self.position.x = max(0, self.mario.position.x - self.view_rect.width // 4)
        self.position.y = 0  # todo: any case where this isn't y?

    def despawn_mario(self):
        assert self.mario.enabled

        # mario handles his own registration
        self.mario.enabled = False

    def serialize(self):
        return {"name": "unknown",
                "filename": self.filename,
                "background_color": (self.background_color[0], self.background_color[1], self.background_color[2]),
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
        spawn_point = self._find_spawn_point()

        if spawn_point:
            self.spawn_mario(spawn_point)

    def _find_spawn_point(self):
        spawn_points = self.entity_manager.search_by_type(MarioSpawnPoint)

        # order spawn points by x location
        spawn_points.sort(key=lambda spawn: spawn.position.x)

        # eliminate spawn points we haven't reached yet
        reached = [sp for sp in spawn_points if sp.position.x <= self.position.x]

        if reached:
            return reached[len(reached) - 1]  # choose the rightmost reached spawn location

        # otherwise, we haven't reached any spawn points. But there might be one visible
        # on screen. Try that one next
        visible = [sp for sp in spawn_points if self.position.x <= sp.position.x <= self.position.x + self.view_rect.width]

        if visible:
            return visible[len(visible) - 1]

        # nothing visible, no checkpoints reached -> just don't spawn mario

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
