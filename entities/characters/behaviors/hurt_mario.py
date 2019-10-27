from .behavior import Behavior
from entities.collider import Collider, ColliderManager, Collision
from entities import Layer
from util import make_vector
import config


class HurtMario(Behavior):
    def __init__(self, entity, collision_manager: ColliderManager, hitbox_offset, hitbox_size):
        super().__init__()

        # note to self: hitbox offset should be unscaled (so it's based on the disk-size sprites, not the rescaled ones)

        self.entity = entity
        self.hitbox = Collider.from_entity(entity, collision_manager, Layer.Mario)
        self.hitbox.rect.size = hitbox_size[0] * config.rescale_factor, hitbox_size[1] * config.rescale_factor
        self.hitbox.on_collision = self._hurt_mario
        self.hitbox_offset = make_vector(hitbox_offset[0] * config.rescale_factor,
                                         hitbox_offset[1] * config.rescale_factor)

    def update(self, dt):
        self.hitbox.move(self.entity.position + self.hitbox_offset, tf_dispatch_events=True)

    def draw(self, screen, view_rect):
        if config.debug_hitboxes:
            screen.fill((0, 255, 0), self.hitbox.rect)

    @staticmethod
    def _hurt_mario(collision):
        print("hurt mario now")
