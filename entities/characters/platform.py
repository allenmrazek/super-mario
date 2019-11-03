import math
from .level_entity import LevelEntity
from util import world_to_screen, mario_str_to_pixel_value_velocity as mstpvv
import constants
from .mario.mario_constants import air_max_vertical_velocity
import config
from util import get_aligned_foot_position, make_vector


class Platform(LevelEntity):
    FALL_RATE = mstpvv('00500')

    """A horizontal platform that moves downward as mario stands on it"""
    def __init__(self, level):
        self.animation = level.asset_manager.interactive_atlas.load_static("horizontal_platform")

        super().__init__(self.animation.get_rect())

        self.level = level

        from entities.collider import Collider
        from entities.characters.behaviors import Interactive

        # need to register a collider in the world for mario to stand on
        self.collider = Collider.from_entity(self, level.collider_manager, 0)
        level.collider_manager.register(self.collider)

        # now another collider to let us know when to drop the platform
        # remember: it assumes unscaled values, while animation has been scaled
        self.platform_tester = Interactive(level, self,
                                           (0, -1),
                                           (self.rect.width / config.rescale_factor,
                                            self.rect.height / config.rescale_factor), self.attach_mario)


        # state
        self._attached = False

    def attach_mario(self, collision):
        mario = self.level.mario

        self._attached = mario.vertical_speed >= 0
        
    def update(self, dt, view_rect):
        # is mario standing on the platform?
        mario = self.level.mario

        if mario.vertical_speed >= 0. and self.pl

        mario_foot_y = mario.movement.get_foot_position().y

        if self._dropping and math.fabs(mario_foot_y - self.position.y) < 1. and mario.vertical_speed >= 0.:
            # mario's on the platform...
            pos = self.position
            pos.y += Platform.FALL_RATE * dt
            self.position = pos
            self.collider.position = self.position

            # align mario to the platform, unless platform drop rate exceeds mario's maximum velocity
            if Platform.FALL_RATE <= air_max_vertical_velocity:
                # if our fall rate doesn't exceed mario's gravity, glue his feet to the platform
                # todo: this will drag him into solid blocks, so fix or don't put these platforms over solid blocks..

                # want to align mario's feet with our top
                new_foot = pos.y - (mario_foot_y - mario.position.y)
                # #aligned = get_aligned_foot_position(self.rect, mario.rect)
                # print("aligning")
                #
                mario.position = make_vector(mario.position.x, new_foot)  # only align y, don't center mario on plat
                mario.movement.update_airborne_status()
            elif mario.movement.is_airborne:
                print("ab")
        elif self._dropping:
            print("dropping, with mario foot", mario_foot_y, " and us", self.position.y)


    def on_mario_standing(self, collision):
        self._dropping = True

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

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