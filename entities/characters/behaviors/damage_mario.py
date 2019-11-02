from ...effects import MarioDeath
from ...effects import MarioTransformSmall
from .interactive import Interactive


class DamageMario(Interactive):
    """A hitbox which will damage mario, if he is not invincible"""
    def __init__(self, level, entity, hitbox_offset, hitbox_size, on_mario_invincible):
        super().__init__(level, entity, hitbox_offset, hitbox_size, self.on_mario_collision)

        self.on_invincible = on_mario_invincible

    def on_mario_collision(self, collision):
        mario = collision.hit_collider.entity

        if not mario.is_invincible and not mario.is_starman:
            DamageMario.hurt_mario(self.level, mario)
        elif self.on_invincible:
            self.on_invincible(collision)

    def destroy(self):
        pass

    @staticmethod
    def hurt_mario(level, mario):
        # returns true if mario is killed

        if mario.is_super:
            # downgrade mario to regular mario
            MarioTransformSmall.apply_transform(level, mario)
            return False
        else:
            level.despawn_mario()
            level.entity_manager.register(MarioDeath(level, level.mario.position))
            return False
