from util import make_vector
from ..entity import Entity
import constants
from util import world_to_screen


class Fireball(Entity):
    LIFETIME = 10.

    def __init__(self, level, parameters, initial_velocity):
        self.animation = level.asset_manager.interactive_atlas.load_animation("fireball")

        super().__init__(self.animation.get_rect())

        self.parameters = parameters
        self.level = level

        from .behaviors import SimpleMovement

        self.movement = SimpleMovement(self, level.collider_manager, parameters,
                                       on_collision_callback=self.on_collision)
        self.movement.horizontal_movement_collider.mask |= constants.Enemy

        self.movement.velocity = initial_velocity

        self._duration = Fireball.LIFETIME
        self._dead = False

        # todo: die when offscreen

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

    def update(self, dt, view_rect):
        self.animation.update(dt)
        self.movement.update(dt)

        if not self.movement.is_airborne:
            self.movement.velocity = make_vector(self.movement.velocity.x, -self.parameters.jump_velocity)

        self._duration -= dt

        if not self._dead and self._duration < 0:
            self.explode()

    def on_collision(self, collision):
        if self._dead:
            return

        if collision.hit_block or (collision.hit_collider and collision.hit_collider.entity.layer == constants.Block):
            self.explode()
        elif collision.hit_collider:
            thing_hit = collision.hit_collider.entity

            die = getattr(thing_hit, "die", None)

            if die:
                die()
                self.explode()
            else:
                print("hit something, but no death function")

    def explode(self):
        self._dead = True

        self.level.entity_manager.unregister(self)

        explode_anim = self.level.asset_manager.interactive_atlas.load_animation("fireball_explode")

        from .corpse import Corpse

        explosion = Corpse(self.level, explode_anim, Corpse.STATIONARY, explode_anim.duration, True)
        explosion.position = self.position + make_vector(self.rect.width // 2, self.rect.height // 2) -\
                             make_vector(explosion.rect.width // 2, explosion.rect.height // 2)

        self.level.entity_manager.register(explosion)
