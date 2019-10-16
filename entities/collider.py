from enum import Enum
from util import can_collide


class Collision:
    def __init__(self, moved_collider, hit_collider):
        self.moving_entity = moved_collider.entity
        self.stationary_entity = hit_collider.entity
        self.moving_collider = moved_collider
        self.stationary_collider = hit_collider


# class CollisionLayer(Enum):
#     Nothing = 0
#     Mario = 1
#     Block = 2


class Collider:
    def __init__(self, entity, manager, mask):
        assert entity is not None
        assert manager is not None
        assert isinstance(mask, int)

        self.entity = entity
        self.manager = manager
        self.mask = mask

    def move(self, new_pixel_position):
        return self.manager.move_collider(self, new_pixel_position)

    @property
    def layer(self):
        return self.entity.layer

    @property
    def rect(self):
        return self.entity.rect


class ColliderManager:
    def __init__(self):
        self._colliders = set()

    def register(self, collider: Collider):
        self._colliders.add(collider)

    def unregister(self, collider: Collider):
        self._colliders.remove(collider)

    def move_collider(self, collider, new_pixel_position):
        collider.rect.x, collider.rect.y = int(new_pixel_position.x), int(new_pixel_position.y)
        collisions = []

        for other_collider in (c for c in self._colliders if c is not collider):
            if not can_collide(collider.mask, other_collider.layer):
                continue

            if collider.rect.colliderect(other_collider.rect) and other_collider not in collisions:
                collisions.append(Collision(collider, other_collider))

        return collisions
