import random
from .behavior import Behavior
from .gravity_movement import GravityMovement
from util import make_vector
import config


class BowserLogic(Behavior):
    TIME_TO_JUMP_MIN = 1
    TIME_TO_JUMP_MAX = 2.5
    FIREBALL_MIN_TIME = 2.25
    FIREBALL_MAX_TIME = 5.50
    MOUTH_OPEN_DURATION = 0.1
    MOVE_TIME = 1.5

    def __init__(self, entity, level, movement):
        super().__init__()

        self.level = level
        self.entity = entity
        self.movement = movement

        # state
        self._time_to_next_jump = BowserLogic.TIME_TO_JUMP_MIN
        self._time_to_fire = BowserLogic.FIREBALL_MIN_TIME
        self._time_since_firing = BowserLogic.MOUTH_OPEN_DURATION
        self._time_moving = 0.
        self.entity.velocity = make_vector(-self.movement.parameters.max_horizontal_velocity, 0.)

    def update(self, dt):
        self._time_moving += dt

        if self._time_moving > BowserLogic.MOVE_TIME and not self.movement.is_airborne:
            self._time_moving = 0.
            self.entity.velocity = make_vector(self.entity.velocity.x * -1, self.entity.velocity.y)

        if not self.movement.is_airborne:
            self._time_to_next_jump -= dt

            if self._time_to_next_jump <= 0.:
                self.jump()

        self._time_to_fire -= dt
        self._time_since_firing += dt

        if self._time_to_fire <= 0.:
            self.fire()

    def draw(self, screen, view_rect):
        pass

    def jump(self):
        self.entity.velocity = make_vector(self.entity.velocity.x, -self.movement.parameters.jump_velocity)
        self._time_to_next_jump = random.uniform(BowserLogic.TIME_TO_JUMP_MIN, BowserLogic.TIME_TO_JUMP_MAX)

    def destroy(self):
        pass

    def fire(self):
        # spawn a seeking fireball
        from ..bowser_fireball import BowserFireball

        # todo: don't fire if mario offscreen?
        fb = BowserFireball(self.level)
        fb.position = make_vector(*self.entity.rect.midtop) + \
                      make_vector(8 * config.rescale_factor - fb.rect.width, 10 * config.rescale_factor)  # offset mouth pos

        self.level.entity_manager.register(fb)
        self.level.asset_manager.sounds['bowserfire'].play()

        self._time_to_fire = random.uniform(BowserLogic.FIREBALL_MIN_TIME, BowserLogic.FIREBALL_MAX_TIME)
        self._time_since_firing = 0.

    @property
    def fired_recently(self):
        return self._time_since_firing < BowserLogic.MOUTH_OPEN_DURATION
