from .level_entity import LevelEntity
from util import world_to_screen, mario_str_to_pixel_value_velocity as mstpvv
import constants
from .mario.mario_constants import air_max_vertical_velocity
import config
from util import make_vector


class Platform(LevelEntity):
    FALL_RATE = mstpvv('01500')

    """A horizontal platform that moves downward as mario stands on it"""
    def __init__(self, level):
        self.animation = level.asset_manager.interactive_atlas.load_static("horizontal_platform")

        super().__init__(self.animation.get_rect())

        self.level = level

        from entities.collider import Collider
        from entities.characters.behaviors import Interactive

        # need to register a collider in the world for mario to stand on
        self.collider = Collider.from_entity(self, level.collider_manager, constants.Block)
        level.collider_manager.register(self.collider)

        # now another collider to let us know when to drop the platform
        # remember: it assumes unscaled values, while animation has been scaled
        self.platform_tester = Interactive(level, self,
                                           (0, -3),
                                           (self.rect.width / config.rescale_factor,
                                            self.rect.height / config.rescale_factor),
                                           self.attach_mario,
                                           self.detach_mario)

        # state
        self._attached = False
        self._pushed = False

    def attach_mario(self, collision):
        mario = self.level.mario

        mario.glued = mario.vertical_speed >= 0 and air_max_vertical_velocity >= Platform.FALL_RATE

    def detach_mario(self):
        self.level.mario.glued = False

    def update(self, dt, view_rect):
        self.collider.position = self.position

        # is mario standing on the platform?
        self.platform_tester.update(dt)

        mario = self.level.mario
        mario_foot_y = mario.movement.get_foot_position().y

        if mario.glued or self._pushed:

            # todo: platform can drag mario into solid blocks, fix

            pos = self.position
            pos.y += Platform.FALL_RATE * dt

            for collision in self.collider.try_move(pos, True):
                if collision.hit_collider and collision.hit_collider.entity:
                    thing_hit = collision.hit_collider.entity

                    if isinstance(thing_hit, Platform):
                        # shove it out of the way
                        thing_hit.position = make_vector(thing_hit.position.x,
                                                         thing_hit.position.y + Platform.FALL_RATE * dt)
                    else:
                        self.collider.position = self.position  # todo: better way to handle this? hit a block

            self.position = self.collider.position

            # want to align mario's feet with our top if he's glued onto the platform
            if mario.glued:
                # mario has been glued onto the platform, we're responsible for moving him (ypos) now
                mario.movement.set_foot_y_coord(self.position.y)

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))
        self.platform_tester.draw(screen, view_rect)

    @property
    def layer(self):
        return constants.Block

    def destroy(self):
        self.level.collider_manager.unregister(self.collider)
        self.level.entity_manager.unregister(self)

    def create_preview(self):
        return self.animation.image.copy()

    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, val):
        super(Platform, self.__class__).position.fset(self, val)
        self.collider.position = val


LevelEntity.create_generic_factory(Platform)
