import math
from entities import Entity, Layer
from entities import Collider, ColliderManager
from .enemy_constants import goomba_parameters
from util import make_vector


class Goomba(Entity):
    def __init__(self, assets, collider_manager):
        self.animation = assets.character_atlas.load_animation("goomba")

        super().__init__(self.animation.get_rect())

        self.movement_collider = Collider.from_entity(self, collider_manager, Layer.Block | Layer.Enemy)
        self.airborne_collider = Collider.from_entity(self, collider_manager, Layer.Block)

        self.movement_collider.on_collision = self._on_hit

        collider_manager.register(self.movement_collider)

        self.parameters = goomba_parameters
        self.velocity = make_vector(self.parameters.max_horizontal_velocity, 0)
        self.movement_collider.on_collision = self._on_hit
        self.airborne = False

        # private state
        self._reverse_direction = False

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self._handle_horizontal_movement(dt)
        self._handle_vertical_movement(dt)

        if not self.airborne:
            self.animation.update(dt)  # only move legs if on the ground

    def _handle_vertical_movement(self, dt):
        # todo: what if it jumps onto another enemy?
        if self._reverse_direction:
            self._reverse_direction = False
            self.velocity.x *= -1.

        self.airborne = self.velocity.y < 0. or not any(self.airborne_collider.test(self.position + make_vector(0, 1)))

        if not self.airborne:
            self.velocity.y = 0
        else:
            self.velocity.y += (self.parameters.gravity * dt)

            # if math.fabs(self.velocity.y) > self.parameters.max_vertical_velocity:
            #     # little note to remind me later to look at any edge cases if they happen
            #     if self.velocity.y < 0:
            #         print("warning: capping max upwards velocity")
            #
            #     self.velocity.y = math.copysign(self.parameters.max_vertical_velocity, self.velocity.y)

        vel = make_vector(0, self.velocity.y)
        target_pos = self.position + vel * dt
        self.movement_collider.position = self.position
        collisions = self.movement_collider.try_move(target_pos, False)

        if collisions:  # couldn't get that close: try and move as close as we can
            # note: we don't set airborne here because it's possible it wasn't a block that prevented movement
            self.movement_collider.iterative_move(target_pos)
            ColliderManager.dispatch_events(self.movement_collider, collisions)

        self.position = self.movement_collider.position

    def _handle_horizontal_movement(self, dt):
        vel = make_vector(self.velocity.x, 0)
        self.movement_collider.position = self.position

        target = self.position + vel * dt

        collisions = self.movement_collider.try_move(target, True)

        if collisions:
            self.movement_collider.iterative_move(target)
            ColliderManager.dispatch_events(self.movement_collider, collisions)

        self.position = self.movement_collider.position

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.animation.image, make_vector(*self.position) - make_vector(*view_rect.topleft))
        self.debug_collision(screen)

    def _on_hit(self, collision):
        if collision.hit_block:
            # we hit a block, but it could have been from above. Determine if block is left or right
            is_left = any(self.airborne_collider.test(self.position - make_vector(1, 0)))
            is_right = any(self.airborne_collider.test(self.position + make_vector(1, 0)))

            # only flip directions if it will improve situation
            if (is_left and self.velocity.x < 0.) or (is_right and self.velocity.x > 0.):
                self._reverse_direction = True
        elif collision.hit_collider is not None and collision.hit_collider.layer == Layer.Enemy:
            self._reverse_direction = True

    @property
    def layer(self):
        return Layer.Enemy

    def debug_collision(self, screen):
        left, right = self.rect.left // 32, self.rect.right // 32
        top, bottom = self.rect.top // 32, self.rect.bottom // 32

        import pygame

        # for x in range(left, right + 1):
        #     for y in range(top, bottom + 1):
        #         r = pygame.Rect(x * 32, y * 32, 32, 32)
        #
        #         screen.fill((255, 0, 255), r)
