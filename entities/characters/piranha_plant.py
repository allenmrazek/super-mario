from entities.entity import Entity
from util import world_to_screen, make_vector
import constants


class PiranhaPlant(Entity):
    EXTEND_PARAMETERS = (1.25, 1.0)  # time to extend, time to stay extended
    RETRACT_PARAMETERS = (0.25, 1.5)
    TIME = 1
    RETRACT_TIME = 1.25

    def __init__(self, level, visible_rect):
        self.animation = level.asset_manager.character_atlas.load_animation("piranha_plant")
        self.level = level

        super().__init__(self.animation.rect)

        from entities.characters.behaviors import DamageMario
        from entities.collider import Collider

        self.position_collider = Collider.from_entity(self, level.collider_manager, 0)
        self.level.collider_manager.register(self.position_collider)

        self.harm = DamageMario(level, self, (3, 9), (12, 12), self.on_mario_invincible)
        self.visible_rect = visible_rect

        # state
        self._emerging = True
        self._timer = 0.
        self._killself = False

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.animation.update(dt)
        self.harm.update(dt)

        self._timer += dt

        fraction_hidden = 0.

        if self._emerging:
            fraction_hidden = 1 - min(self._timer / PiranhaPlant.EXTEND_PARAMETERS[0], 1.)
            if self._timer > sum(PiranhaPlant.EXTEND_PARAMETERS):
                self._timer = 0.
                self._emerging = False
        else:  # must be retracting
            fraction_hidden = min(self._timer / PiranhaPlant.RETRACT_PARAMETERS[0], 1.)

            if self._timer > sum(PiranhaPlant.RETRACT_PARAMETERS):
                self._timer = 0
                self._emerging = True

        self.position = make_vector(self.visible_rect.left, self.visible_rect.top + self.rect.height * fraction_hidden)
        self.position_collider.position = self.position

    def draw(self, screen, view_rect):
        draw_rect = self.rect.clip(self.visible_rect)

        draw_rect.x, draw_rect.y = world_to_screen(self.position, view_rect)
        src_rect = self.animation.get_rect()
        src_rect.width, src_rect.height = draw_rect.width, draw_rect.height

        screen.blit(self.animation.image, draw_rect, src_rect)
        self.harm.draw(screen, view_rect)

    def destroy(self):
        self.level.collider_manager.unregister(self.position_collider)
        self.level.entity_manager.unregister(self)

    def on_mario_invincible(self, collision):
        mario = self.level.mario

        if mario.is_starman:
            self.die()

    def die(self):
        self.destroy()
        self.level.asset_manager.sounds['stomp'].play()  # just disappears? todo: investigate death of piranha plant

    @property
    def layer(self):
        return constants.Enemy
