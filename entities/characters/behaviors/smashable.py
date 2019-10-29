from .interactive import Interactive
from entities.collider import Collider, Collision
from .behavior import Behavior
from util import make_vector, rescale_vector, world_to_screen, pixel_coords_to_tile_coords, distance_squared, tile_coords_to_pixel_coords
from entities.entity import Layer
import config


class Smashable(Behavior):
    def __init__(self, level, entity, on_head_smash):
        super().__init__()

        # create a collider in the world that can receive events
        self.level = level
        self.entity = entity
        self.hitbox = Collider(entity, self.level.collider_manager,
                               Layer.Mario, entity.position, entity.rect, Layer.Block, self._on_mario_hit)

        self.hitbox.position = entity.position
        self.on_head_smash = on_head_smash

        self.level.collider_manager.register(self.hitbox)

        # state
        self._smashed = False

    def destroy(self):
        super().destroy()
        self.level.collider_manager.unregister(self.hitbox)

    def update(self, dt):
        self.hitbox.position = self.entity.position

        if self._smashed:
            self.on_head_smash()
            self._smashed = False

    def draw(self, screen, view_rect):
        if config.debug_hitboxes:
            r = self.hitbox.rect.copy()
            self.hitbox.position = self.entity.position
            r.topleft = world_to_screen(self.hitbox.position, view_rect)
            r = screen.get_rect().clip(r)
            screen.fill((0, 255, 0), r)

    def _on_mario_hit(self, collision):
        # determine whether mario hit the bottom of this block with his head
        # for this to occur, the following things must be true:
        #   mario's velocity is negative (meaning he's moving up)
        #   mario must be airborne
        #   mario must intersect some portion of our collider directly below us
        #   mario must be in the same grid square (horizontally) as us if mario is hitting more than one block
        mario = collision.moved_collider.entity

        if mario.vertical_speed >= 0:
            return

        target = self.hitbox.position + make_vector(0, self.hitbox.rect.height)

        if not self.hitbox.test(target, False):
            return

        #  now check to see who gets smashed...
        mario_center = make_vector(*mario.rect.center)
        mario_coords = pixel_coords_to_tile_coords(mario_center, self.level.tile_map.tileset)

        our_center = make_vector(*collision.hit_collider.entity.rect.center)
        our_coords = pixel_coords_to_tile_coords(our_center, self.level.tile_map.tileset)

        if mario_coords[0] == our_coords[0]:
            # it's definitely us. don't destroy immediately though: if mario hit multiple bricks, removing
            # our collider too early might trick them into blowing up too
            self._smashed = True
            mario.bounce(0)
        else:
            def get_position(coll: Collision):
                if coll.hit_collider is None:
                    return tile_coords_to_pixel_coords(coll.hit_block, self.level.tile_map.tileset)
                else:
                    return make_vector(*coll.hit_collider.rect.center)

            # find out if there are any other candidates
            # note: if the moved collider is dispatching events after an iterative move, it's
            # quite possible that where that collider is _now_ isn't what caused a collision. Hence,
            # its position when a collision happened is stored
            collisions = collision.moved_collider.test(collision.moved_collider_position)

            if len(collisions) == 1:
                # we know this is us
                self._smashed = True
                mario.bounce(0)
            elif len(collisions) > 0:
                # the closest (by center) should receive this hit
                collisions.sort(key=lambda c2: distance_squared(mario_center, get_position(c2)))

                if collisions[0].hit_collider is self:
                    self._smashed = True
