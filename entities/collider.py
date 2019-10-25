import math
from util import can_collide
from util import distance_squared
from util import copy_vector
from entities.entity import Layer
import config


class Collision:
    __slots__ = ['moved_collider', 'hit_thing']

    def __init__(self, moved_collider, hit_thing):
        self.moved_collider = moved_collider
        self.hit_thing = hit_thing  # not necessarily a collider or entity (could be a grid position)


class Collider:
    """A collider is not much more than a fancy rect controlled by some parent entity. Entities can use colliders
    to test for collisions against other colliders.  Every collider is associated with some entity (entities can have
    multiple colliders associated with them)"""
    __slots__ = ['entity', 'manager', 'mask', '_position', 'rect', 'layer']

    """Important note: Colliders are intended to be managed by their associated Entity"""
    def __init__(self, entity, manager, mask, position, rect, layer):
        assert entity is not None
        assert manager is not None
        assert isinstance(mask, int)

        self.entity = entity
        self.manager = manager
        self.mask = mask or 0
        self._position = copy_vector(position)
        self.rect = rect.copy()
        self.layer = layer

    @staticmethod
    def from_entity(entity, manager, mask):
        assert entity is not None
        assert isinstance(manager, ColliderManager)

        return Collider(entity, manager, mask or 0, entity.position, entity.rect, entity.layer)

    def move(self, new_pixel_position):
        return self.manager.move(self, new_pixel_position)

    def try_move(self, new_pixel_position):
        return self.manager.try_move(self, new_pixel_position)

    def test(self, new_pixel_position):
        return self.manager.test(self, new_pixel_position)

    def iterative_move(self, new_pixel_position):
        return self.manager.iterative_move(self, new_pixel_position)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val
        self.rect.x, self.rect.y = self._position.x, self._position.y


class ColliderManager:
    """Colliders use an instance of this to test against other colliders"""
    def __init__(self, map):
        self._colliders = set()
        self.map = map

    def register(self, collider: Collider):
        self._colliders.add(collider)

    def unregister(self, collider: Collider):
        self._colliders.remove(collider)

    def move(self, collider, new_pixel_position):
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
                collisions.append(Collision(collider, other_collider))

        return collisions

    def try_move(self, collider, new_pixel_position):
        """Teleports collider to new position. If there are any collisions, the
        collider's position IS NOT MODIFIED"""
        pos = collider.position

        collisions = self.move(collider, new_pixel_position)

        if collisions:
            # undo movement
            collider.position = pos

        return collisions

    def test(self, collider, new_pixel_position):
        """Tests a collider at a position for collisions. Does not modify collider"""
        pos = collider.position
        collisions = self.move(collider, new_pixel_position)
        collider.position = pos

        return collisions

    def iterative_move(self, collider, new_pixel_position, iterations=config.PHYSICS_COLLISION_ITERATIONS):
        """Special type of move that advances towards coordinates by teleporting repeatedly. If the first teleport
        hits something, distance is halved and the move is attempted again. If no movement could be made, returns
        current collision values"""
        initial = collider.position

        dsquared = distance_squared(initial, new_pixel_position)
        if dsquared < 1.:
            return []

        dist = math.sqrt(dsquared)
        direction = (new_pixel_position - initial).normalize()
        collisions = []

        for _ in range(iterations):
            collisions = self.try_move(collider, initial + direction * dist)

            if len(collisions) == 0:
                break
            else:
                # halve distance
                dist *= 0.5

        return collisions

    def get_world_collisions(self, collider):
        # determine which grid square(s) the collider is in
        left, right = collider.rect.left // self.map.tile_width, collider.rect.right // self.map.tile_width
        top, bottom = collider.rect.top // self.map.tile_height, collider.rect.bottom // self.map.tile_height

        collisions = []

        for x in range(left, right + 1):
            if x < 0 or x >= self.map.width:
                continue

            for y in range(top, bottom + 1):
                if y < 0 or y >= self.map.height:
                    continue

                if not self.map.get_passable((x, y)):
                    collisions.append(Collision(moved_collider=collider, hit_thing=(x, y)))

        return collisions
