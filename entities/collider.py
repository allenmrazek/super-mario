import math
import sys
import copy
from pygame import Rect
from util import can_collide
from util import distance_squared
from util import copy_vector
from entities.entity import Layer
import config

epsilon_sqr = sys.float_info.epsilon ** 2


def value_in_range(value, min_value, max_value):
    return (value >= min_value) and (value <= max_value)


def rect_overlap(A, B):
    x_overlap = value_in_range(A.x, B.x, B.x + B.width) or value_in_range(B.x, A.x, A.x + A.width)
    y_overlap = value_in_range(A.y, B.y, B.y + B.height) or value_in_range(B.y, A.y, A.y + A.height)

    return x_overlap and y_overlap


class Collision:
    __slots__ = ['moved_collider', 'hit_collider', 'hit_block', 'moved_collider_position']

    def __init__(self, moved_collider, hit_thing, moved_collider_position):
        self.hit_collider = hit_thing if isinstance(hit_thing, Collider) else None
        self.hit_block = hit_thing if isinstance(hit_thing, tuple) else None
        self.moved_collider_position = moved_collider_position
        self.moved_collider = moved_collider


class Collider:
    """A collider is not much more than a fancy rect controlled by some parent entity. Entities can use colliders
    to test for collisions against other colliders.  Every collider is associated with some entity (entities can have
    multiple colliders associated with them)"""
    __slots__ = ['entity', 'manager', 'mask', '_position', 'rect', 'layer', 'on_collision']

    """Important note: Colliders are intended to be managed by their associated Entity"""
    def __init__(self, entity, manager, mask, position, rect, layer, on_collision_callback=None):
        assert entity is not None
        assert manager is not None
        assert isinstance(mask, int)

        self.entity = entity
        self.manager = manager
        self.mask = mask or 0
        self._position = copy_vector(position)
        self.rect = rect.copy()
        self.layer = layer
        self.on_collision = on_collision_callback

    @staticmethod
    def from_entity(entity, manager, mask):
        assert entity is not None
        assert isinstance(manager, ColliderManager)

        return Collider(entity, manager, mask or 0, entity.position, entity.rect, entity.layer)

    def move(self, new_pixel_position, tf_dispatch_events=False):
        return self.manager.move(self, new_pixel_position, tf_dispatch_events)

    def try_move(self, new_pixel_position, tf_dispatch_events=False):
        return self.manager.try_move(self, new_pixel_position, tf_dispatch_events)

    def test(self, new_pixel_position, tf_dispatch_events=False):
        return self.manager.test(self, new_pixel_position, tf_dispatch_events)

    def iterative_move(self, new_pixel_position, tf_dispatch_events=False):
        return self.manager.iterative_move(self, new_pixel_position, tf_dispatch_events=tf_dispatch_events)

    def approach(self, new_pixel_position, tf_dispatch_events=False):
        collisions = self.try_move(new_pixel_position, tf_dispatch_events=False)

        if collisions:
            self.iterative_move(new_pixel_position, False)

            if tf_dispatch_events:
                ColliderManager.dispatch_events(self, collisions)

        return collisions

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val
        self.rect.x, self.rect.y = self._position.x, self._position.y


class ColliderManager:
    """Colliders use an instance of this to test against other colliders"""
    def __init__(self, tile_map):
        self._colliders = set()
        self.tile_map = tile_map

    def register(self, collider: Collider):
        self._colliders.add(collider)

    def unregister(self, collider: Collider):
        self._colliders.remove(collider)

    def contains(self, collider):
        return collider in self._colliders

    def move(self, collider, new_pixel_position, tf_dispatch_events=False):
        """Teleports the collider to new position, and returns any resulting collisions"""
        collider.position = copy_vector(new_pixel_position)
        collider.rect.x, collider.rect.y = collider.position.x, collider.position.y
        collisions = []

        # check for collisions against world grid, if applicable
        if can_collide(collider.mask, Layer.Block.value):
            collisions.extend(self.get_world_collisions(collider))

        for other_collider in (c for c in self._colliders if c is not collider):
            if not can_collide(collider.mask, other_collider.layer):
                continue

            if collider.rect.colliderect(other_collider.rect) and other_collider not in collisions:
                collisions.append(Collision(collider, other_collider, copy_vector(collider.position)))

        if tf_dispatch_events:
            ColliderManager.dispatch_events(collider, collisions)

        return collisions

    def try_move(self, collider, new_pixel_position, tf_dispatch_events=False):
        """Teleports collider to new position. If there are any collisions, the
        collider's position IS NOT MODIFIED"""
        pos = collider.position

        collisions = self.move(collider, new_pixel_position, tf_dispatch_events=tf_dispatch_events)

        if collisions:
            # undo movement
            collider.position = pos

        if tf_dispatch_events:
            ColliderManager.dispatch_events(collider, collisions)

        return collisions

    def test(self, collider, new_pixel_position, tf_dispatch_events=False):
        """Tests a collider at a position for collisions. Does not modify collider"""
        pos = collider.position
        collisions = self.move(collider, new_pixel_position)
        collider.position = pos

        if tf_dispatch_events:
            ColliderManager.dispatch_events(collider, collisions)

        return collisions

    def iterative_move(self, collider, new_pixel_position, tf_dispatch_events=False):
        """Special type of move that advances towards coordinates by teleporting repeatedly. If the first teleport
        hits something, distance is halved and the move is attempted again. Returns amount moved"""
        initial = collider.position

        dsquared = distance_squared(initial, new_pixel_position)
        if dsquared < epsilon_sqr:
            return []

        dist = math.sqrt(dsquared)
        direction = (new_pixel_position - initial).normalize()

        while True:
            collisions = self.try_move(collider, initial + direction * dist)

            if len(collisions) == 0:
                break
            else:
                # halve distance
                dist *= 0.5

                if dist < 0.05:
                    break

        if tf_dispatch_events:
            ColliderManager.dispatch_events(collider, collisions)

        return dist

    def get_world_collisions(self, collider):
        # determine which grid square(s) the collider is in
        left, right = int(collider.rect.left / self.tile_map.tile_width), int(collider.rect.right / self.tile_map.tile_width)
        top, bottom = int(collider.rect.top / self.tile_map.tile_height), int(collider.rect.bottom / self.tile_map.tile_height)

        collisions = []
        r = Rect(left * self.tile_map.tile_width, top * self.tile_map.tile_height, self.tile_map.tile_width, self.tile_map.tile_height)

        # each of these tiles is potentially intersecting the collider
        for x in range(left, right + 1):
            if x < 0 or x >= self.tile_map.width:
                continue

            for y in range(top, bottom + 1):
                if y < 0 or y >= self.tile_map.height:
                    continue

                if not self.tile_map.get_passable((x, y)):
                    # a non-passable tile might be within range: now use a pixel-perfect collision test
                    r.x = x * self.tile_map.tile_width
                    r.y = y * self.tile_map.tile_height

                    if collider.rect.colliderect(r):
                        collisions.append(Collision(moved_collider=collider, hit_thing=(x, y), moved_collider_position=copy_vector(collider.position)))

        return collisions

    def colliders(self):
        return copy.copy(self._colliders)

    @staticmethod
    def dispatch_events(collider, collisions):
        for c in collisions:
            #if collider.on_collision is not None and c.hit_collider is not collider:
            #collider.on_collision(c)

            if c.hit_collider is not None and c.hit_collider.on_collision is not None:
                c.hit_collider.on_collision(c)

