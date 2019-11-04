import math
from util import make_vector
import constants
from .projectile import Projectile
from .parameters import CharacterParameters
from util import mario_str_to_pixel_value_velocity as mstpvv
from ..collider import Collider
import config

bowser_fb_parameters = CharacterParameters(mstpvv('00800'), mstpvv('01600'), 0., 0., 0.)


class BowserFireball(Projectile):
    """Bowser's tracking fireball"""
    TRACK_VELOCITY = mstpvv('01200')  # how quickly the fireball can alter position to track mario
    TARGET_ACQUIRE_TIME = 0.1         # have to be within lock-on distance for this amount of time before stop tracking
    LOCK_ON_DISTANCE = config.base_tile_dimensions[1] * config.rescale_factor * 0.75

    def __init__(self, level):
        self.animation = level.asset_manager.interactive_atlas.load_animation("bowser_fireball")

        super().__init__(self.animation, level, bowser_fb_parameters, (6, 2), (6, 6), constants.Block, constants.Mario)

        self.level = level
        self.ground_detector = Collider.from_entity(self, level.collider_manager, constants.Block)

        self.movement.velocity = make_vector(-bowser_fb_parameters.max_horizontal_velocity, 0.)

        # state
        self._is_tracking = True
        self._locked_on_time = 0.
        self._dead = False

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        if self._is_tracking:
            mario = self.level.mario

            delta_y = BowserFireball.TRACK_VELOCITY * dt
            mario_y = mario.movement.get_center_of_mass().y

            dist = math.fabs(self.position.y - mario_y)
            if dist < BowserFireball.LOCK_ON_DISTANCE:
                self._locked_on_time += dt

                if self._locked_on_time >= BowserFireball.TARGET_ACQUIRE_TIME:
                    self._is_tracking = False
            else:
                self._locked_on_time = 0.

            if self._is_tracking:
                # approach mario's coordinate
                if dist < delta_y:  # we're close enough to just match it
                    self.position = make_vector(self.position.x, mario_y)
                else:
                    our_pos = self.position

                    our_pos.y += delta_y * (1. if our_pos.y < mario_y else -1.)

                    # move to this position if we can (if there's a block in the way, stay put and stop tracking)
                    if self.ground_detector.test(our_pos, False):
                        # collided!
                        self._is_tracking = False
                    else:
                        self.position = our_pos

    def die(self):
        self.level.entity_manager.unregister(self)
        self.movement.destroy()
        self.level.asset_manager.sounds['stomp'].play()
        self._dead = True

    def on_movement_collision(self, collision):
        if not self._dead:
            self.die()

    def on_hit(self, collision):
        from .behaviors import DamageMario

        mario = self.level.mario

        if mario.is_starman:
            self.die()
        elif not mario.is_invincible:
            DamageMario.hurt_mario(self.level, self.level.mario)
