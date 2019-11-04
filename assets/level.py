import json
import pygame
from pygame import Rect
from entities.collider import ColliderManager, Collider
from assets.tile_map import TileMap
import config
from util import make_vector, copy_vector
import entities.characters
from entities.characters.spawners import MarioSpawnPoint
from entities.characters.mario.mario import Mario
from event import PlayerInputHandler
from event.game_events import EventHandler
import entities.effects.mario_death
import constants


class Level(EventHandler):
    """A level is the highest-level object containing everything that makes up a level"""
    def __init__(self, assets, entity_manager, stats, title="Not Titled"):
        super().__init__()

        assert entity_manager is not None
        assert assets is not None

        self.entity_manager = entity_manager
        self.tile_map = TileMap((60, 20), assets.tileset)
        self.collider_manager = ColliderManager(self.tile_map)
        self.background_color = (0, 0, 0)
        self.filename = ""
        self.normal_physics = True
        self.stats = stats
        self.title = title
        self.loaded_from = ""

        self.asset_manager = assets
        self.player_input = PlayerInputHandler()
        self.mario = Mario(self.player_input, self)
        self.mario.enabled = False

        self._scroll_position = make_vector(0, 0)
        self._view_rect = Rect(0, 0, config.screen_rect.width, config.screen_rect.height)
        self._cleared = False
        self._timed_out = False

    def add_entity(self, entity):
        self.entity_manager.register(entity)

    def update_triggers_only(self, dt):
        # doesn't scroll map or update anything other than triggers
        self.entity_manager.update_layer(constants.Trigger, dt, self.view_rect)

    def update(self, dt):
        self.entity_manager.update(dt, self.view_rect)

        # scroll map with mario
        if self.mario.enabled:
            left = self.mario.position.x - self.view_rect.width // 4

            self.position = make_vector(left if self.position.x < left else self.position.x, 0)

            if self.mario.position.y > self.tile_map.height_pixels + self.mario.rect.height * 4:
                self.despawn_mario()
                self.entity_manager.register(entities.effects.mario_death.MarioDeath(self, self.mario.position))

        if self.stats.remaining_time <= 0:
            self._timed_out = True

    def draw(self, screen):
        vr = self.view_rect  # send copy: don't want our private stuff messed with

        self.tile_map.draw(screen, vr)
        self.entity_manager.draw(screen, vr)

    def handle_event(self, evt, game_events):
        self.player_input.handle_event(evt, game_events)

    def spawn_mario(self, spawn_point=None):
        spawn_point = spawn_point or self._find_spawn_point()

        assert isinstance(spawn_point, MarioSpawnPoint)

        self.mario.enabled = True
        assert self.mario.enabled

        self.mario.position = spawn_point.position
        self.mario.reset()  # reset state

        # prevent mario from phasing into the ground (should he be super mario and the spawn point is on the ground)
        ground_collider = Collider.from_entity(self.mario, self.collider_manager, constants.Block)
        ground_collider.rect.width = 16 * config.rescale_factor
        ground_collider.rect.height = 16 * config.rescale_factor \
            if not self.mario.is_super else 32 * config.rescale_factor
        ground_collider.position = self.mario.position

        tries = 0
        while ground_collider.test(ground_collider.position, False):
            ground_collider.position += make_vector(0, -1)

            tries += 1
            if tries > 1000:
                print("error -- couldn't find suitable spawn location for mario")
                raise RuntimeError

        self.mario.position = ground_collider.position

        # set level scroll position to be one quarter-screen behind mario, unless that would result in left edge
        # of map being visible
        scroll_pos = make_vector(max(0, self.mario.position.x - self.view_rect.width // 4), self.position.y)
        self.position = scroll_pos

    def despawn_mario(self):
        assert self.mario.enabled

        # mario handles his own registration
        self.mario.enabled = False

    def serialize(self):
        return {"name": "unknown",
                "filename": self.filename,
                "normal_physics": self.normal_physics,
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
        self.normal_physics = values["normal_physics"] if "normal_physics" in values else True

        # we only want one unique mario, ignore any that might have been deserialized
        for existing in self.entity_manager.search_by_type(entities.characters.mario.Mario):
            existing.destroy()

        # add our unique mario
        self.entity_manager.register(self.mario)

    def begin(self):
        if self.mario.enabled:
            self.mario.enabled = False

        spawn_point = self._find_spawn_point()

        if spawn_point:
            self.spawn_mario(spawn_point[0])
        else:
            print("warning -- couldn't find mario spawn point")

    def set_cleared(self):
        self._cleared = True

    def reset(self):
        if self.loaded_from:
            current_spawn = self._find_spawn_point()

            self.load_from_path(self.loaded_from, current_spawn[1])  # want idx, not actual point
            self.stats.reset_time()
            self._timed_out = False
            self._cleared = False

        else:
            print("warning: failed to reset level -- was not loaded from disk")

    @property
    def cleared(self):
        return self._cleared

    @property
    def timed_out(self):
        return self._timed_out

    def load_from_path(self, filename, spawn_idx=0):
        self._cleared = False

        self.entity_manager.clear()

        with open(filename, 'r') as f:
            self.deserialize(json.loads(f.read()))

        self.loaded_from = filename

        if spawn_idx > 0:
            spawn_points = self.entity_manager.search_by_type(MarioSpawnPoint)
            spawn_points.sort(key=lambda spawn: spawn.position.x)

            assert len(spawn_points) > 0

            self.position.x = spawn_points[spawn_idx].position.x

    def _find_spawn_point(self):
        spawn_points = self.entity_manager.search_by_type(MarioSpawnPoint)

        # order spawn points by x location
        spawn_points.sort(key=lambda spawn: spawn.position.x)

        # eliminate spawn points we haven't reached yet
        reached = [sp for sp in spawn_points if sp.position.x <= self.position.x]

        if reached:
            return reached[-1], reached.index(reached[-1])  # choose the rightmost reached spawn location

        # otherwise, we haven't reached any spawn points. But there might be one visible
        # on screen. Try that one next
        visible = [sp for sp in spawn_points
                   if self.position.x <= sp.position.x <= self.position.x + self.view_rect.width]

        if visible:
            return visible[-1], visible.index(visible[-1])

        # nothing visible, no checkpoints reached -> use first spawn point
        if len(spawn_points) > 0:
            return spawn_points[0], 0

        print(f"*** warning *** no spawn points found for {self.filename}")

    @property
    def view_rect(self):
        return self._view_rect.copy()

    @property
    def position(self):
        return copy_vector(self._scroll_position)

    @position.setter
    def position(self, new_pos):
        max_w, max_h = self.tile_map.width_pixels - self._view_rect.width, \
                       self.tile_map.height_pixels - self._view_rect.height

        self._scroll_position = make_vector(min(max_w, new_pos[0]), min(max_h, new_pos[1]))
        self._view_rect.topleft = self._scroll_position

    def snapshot(self, filename):
        capture = pygame.Surface((self.tile_map.width_pixels, self.tile_map.height_pixels))
        screen = pygame.Surface(config.screen_size)

        current_pos = self.position

        for x in range(0, capture.get_width() + config.screen_size[0], config.screen_size[0]):
            y = 0  # todo: something broken with painting on y coords, low urgency

            self.position = make_vector(x, y)
            screen.fill(self.background_color)
            self.draw(screen)

            capture.blit(screen, (x, y))

        # restore state
        self.position = current_pos

        # save results
        pygame.image.save(capture, filename)

    @staticmethod
    def take_snapshot(assets, entity_manager, level_filename, save_path):
        lvl = Level(assets, entity_manager, None)
        lvl.load_from_path(level_filename)

        lvl.snapshot(save_path)
