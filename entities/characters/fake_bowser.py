from .enemy import Enemy
from .parameters import CharacterParameters
from util import world_to_screen, mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from .level_entity import LevelEntity
import constants

bowser_parameters = CharacterParameters(
    mstpvv('00500'),
    mstpvv('04000'),
    mstpva('00200'),
    mstpvv('03000'),
    mstpvv('02000'))


class FakeBowser(Enemy):
    BOWSER_HITPOINTS = 5  # number of fireballs needed to kill
    DELAY_LEVEL_END = 3.  # how long to wait after bowser dies to end the level

    def __init__(self, level):
        ca = level.asset_manager.character_atlas

        self.animation_open = ca.load_animation("bowser_left_mouth_open")
        self.animation_close = ca.load_animation("bowser_left_mouth_closed")

        super().__init__(level, self.animation_close.get_rect())

        from .behaviors.bowser_logic import BowserLogic
        from .behaviors.simple_movement import SimpleMovement

        self.level = level
        self.movement = SimpleMovement(self, level.collider_manager, bowser_parameters)
        self.logic = BowserLogic(self, level, self.movement)

        from .behaviors import DamageMario

        # not stompable
        self.head = DamageMario(level, self, (1, 1), (13, 14), self.on_mario_invincible)
        self.body = DamageMario(level, self, (14, 9), (18, 22), self.on_mario_invincible)

        # state
        self.hitpoints = FakeBowser.BOWSER_HITPOINTS

    def update(self, dt, view_rect):
        self.movement.update(dt)
        self.logic.update(dt)
        self.animation_close.update(dt)
        self.animation_open.update(dt)
        self.head.update(dt)
        self.body.update(dt)

    def draw(self, screen, view_rect):
        src = self.animation_open.image if self.logic.fired_recently else self.animation_close.image
        screen.blit(src, world_to_screen(self.position, view_rect))

        self.movement.draw(screen, view_rect)
        self.logic.draw(screen, view_rect)

        self.head.draw(screen, view_rect)
        self.body.draw(screen, view_rect)

    def create_preview(self):
        return self.animation_close.image.copy()

    def destroy(self):
        self.logic.destroy()
        self.movement.destroy()
        self.level.entity_manager.unregister(self)

    def on_mario_invincible(self, collision):
        if self.level.mario.is_starman:
            self.die(force=True)

    def die(self, force=False):
        if not force and not self.level.mario.is_starman:
            self.hitpoints -= 1
            if self.hitpoints > 0:
                return

        self.destroy()

        print("todo: bowser corpse")

        # todo: corpse of underworld goomba

        from .bowser_fireball import BowserFireball

        # destroy all existing bowser fireballs so player doesn't get screwed in their victory
        for fb in self.level.entity_manager.search_by_type(BowserFireball):
            fb.die()

        # end the level
        from .triggers.delay_level_end import DelayLevelEnd
        delay = DelayLevelEnd(self.level, FakeBowser.DELAY_LEVEL_END)
        self.level.entity_manager.register(delay)

    @property
    def layer(self):
        return constants.Enemy


LevelEntity.create_generic_factory(FakeBowser)
