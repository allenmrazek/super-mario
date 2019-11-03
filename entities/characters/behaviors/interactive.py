from .behavior import Behavior
from entities.collider import Collider
from util import world_to_screen, rescale_vector
import config
import constants


class Interactive(Behavior):
    """Invokes a callback when Mario intersects this entity's collider"""
    def __init__(self, level, entity, hitbox_offset, hitbox_size, on_hit, on_not_hit=None):
        super().__init__()

        assert level is not None
        assert entity is not None

        # note to self: hitbox offset should be unscaled (so it's based on the disk-size sprites, not the rescaled ones)

        self.level = level
        self.entity = entity
        self.hitbox = Collider.from_entity(entity, level.collider_manager, constants.Mario)
        self.hitbox.rect.size = rescale_vector(hitbox_size)
        self.hitbox_offset = rescale_vector(hitbox_offset)
        self.hitbox.position = entity.position + self.hitbox_offset
        self.on_hit = on_hit
        self.on_not_hit = on_not_hit

    def update(self, dt):
        if self.on_hit is None:
            return

        collisions = self.hitbox.move(self.entity.position + self.hitbox_offset, True)

        for c in collisions:
            self.on_hit(c)

        if not collisions and self.on_not_hit:
            self.on_not_hit()

    def draw(self, screen, view_rect):
        if config.debug_hitboxes:
            r = self.hitbox.rect.copy()
            self.hitbox.position = self.entity.position + self.hitbox_offset
            r.topleft = world_to_screen(self.hitbox.position, view_rect)
            r = screen.get_rect().clip(r)
            screen.fill((0, 255, 0), r)

    def destroy(self):
        pass
