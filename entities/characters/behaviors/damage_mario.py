from .behavior import Behavior
from ...effects import MarioDeath
from entities.collider import Collider, ColliderManager, Collision
from entities import Layer
from util import make_vector, world_to_screen
import config
from .interactive import Interactive


class DamageMario(Interactive):
    """A hitbox which will damage mario, if he is not invincible"""
    def __init__(self, level, entity, hitbox_offset, hitbox_size):
        super().__init__(level, entity, hitbox_offset, hitbox_size, self.on_mario_collision)

    def on_mario_collision(self, collision):
        # todo: logic which downgrades mario?

        self.level.despawn_mario()
        self.level.entity_manager.register(MarioDeath(self.level, self.level.mario.position))

    def destroy(self):
        pass



# class DamageMario(Behavior):
#     """A hitbox which will damage mario, if he is not invincible"""
#     def __init__(self, level, entity, hitbox_offset, hitbox_size):
#         super().__init__()
#
#         # note to self: hitbox offset should be unscaled (so it's based on the disk-size sprites, not the rescaled ones)
#
#         self.level = level
#         self.entity = entity
#         self.hitbox = Collider.from_entity(entity, level.collider_manager, Layer.Mario)
#         self.hitbox.rect.size = hitbox_size[0] * config.rescale_factor, hitbox_size[1] * config.rescale_factor
#         self.hitbox.on_collision = self.on_mario_collision
#         self.hitbox_offset = make_vector(hitbox_offset[0] * config.rescale_factor,
#                                          hitbox_offset[1] * config.rescale_factor)
#
#     def update(self, dt):
#         self.hitbox.move(self.entity.position + self.hitbox_offset, tf_dispatch_events=True)
#
#     def draw(self, screen, view_rect):
#         if config.debug_hitboxes:
#             r = self.hitbox.rect.copy()
#             self.hitbox.position = self.entity.position + self.hitbox_offset
#             r.topleft = world_to_screen(self.hitbox.position, view_rect)
#             r = screen.get_rect().clip(r)
#             screen.fill((0, 255, 0), r)
#
#     def on_mario_collision(self, collision):
#         # todo: logic which downgrades mario?
#
#         self.level.despawn_mario()
#         self.level.entity_manager.register(MarioDeath(self.level, self.level.mario.position))
#
#     def destroy(self):
#         pass
