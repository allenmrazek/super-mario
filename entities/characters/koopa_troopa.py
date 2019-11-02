from entities.characters.level_entity import LevelEntity
from entities.characters import Corpse
from entities.entity import Entity
from entities.characters.enemy import Enemy
from entities.characters.behaviors import EnemyGroundMovement, Squashable
from . import CharacterParameters
import constants
from util import mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from entities.collider import Collider
from .behaviors import SimpleMovement
from util import get_aligned_foot_position, world_to_screen, make_vector
from .shell import Shell

koopa_parameters = CharacterParameters(10, mstpvv('04800'), mstpva('00300'), 100, mstpvv('04200'))

# todo: red koopa, patrols a set area and doesn't suicide off ledges


class KoopaTroopa(Enemy):
    """Actively walking koopa, green, walks left until defeated or falls"""
    def __init__(self, level):
        self.level = level

        ca = level.asset_manager.character_atlas

        self.left_animation = ca.load_animation("koopa_green_left")
        self.right_animation = ca.load_animation("koopa_green_right")

        super().__init__(level, self.left_animation.get_rect())

        self.movement = EnemyGroundMovement(self, level.collider_manager, koopa_parameters)
        self.squashable = Squashable(level, self, (2, 8), (13, 13), koopa_parameters.squash_bounce_velocity,
                                     self.squash, self._on_mario_invincible)

    @property
    def _animation(self):
        return self.left_animation if self.movement.velocity.x <= 0. else self.right_animation

    def update(self, dt, view_rect):
        self.movement.update(dt)
        self.squashable.update(dt)

        if not self.movement.is_airborne:
            self._animation.update(dt)  # only move legs if on the ground

    def draw(self, screen, view_rect):
        screen.blit(self._animation.image, world_to_screen(self.position, view_rect))
        self.movement.draw(screen, view_rect)
        self.squashable.draw(screen, view_rect)

    def destroy(self):
        super().destroy()
        self.level.entity_manager.unregister(self)
        self.movement.destroy()

    def squash(self):
        mario = self.level.mario

        if mario.is_starman:
            self.die()  # starman doesn't stun koopas, they just die
        else:
            # spawn a stunned koopa
            self.stunned()

    def _on_mario_invincible(self, collision):
        if self.level.mario.is_starman:
            self.die()  # we die, instead of mario dying

    def create_preview(self):
        return self.left_animation.image.copy()

    def stunned(self):
        # create a "stunned" version of the koopa. It will transform back into a koopa if left alone
        stunned = StunnedKoopaTroopa(self.level, self.movement.velocity)
        stunned.position = get_aligned_foot_position(self.rect, stunned.rect)
        self.level.entity_manager.register(stunned)

        self.level.asset_manager.sounds['stomp'].play()

        self.destroy()

    def die(self):
        self.destroy()

        corpse = Corpse.create_ghost_corpse_from_entity(
            self, self.level.asset_manager.character_atlas.load_animation("shell_green"),
            self.level, 5., Corpse.STANDARD)

        self.level.entity_manager.register(corpse)
        self.level.asset_manager.sounds['stomp'].play()

    @property
    def layer(self):
        return constants.Enemy


class StunnedKoopaTroopa(Entity):
    RESPAWN_DELAY = 5  # 5 seconds to respawn
    WARNING_ANIMATION = 2  # when 2 seconds left to respawn, start playing the shell animation

    """This Koopa looks like a green shell on the ground. Does not harm mario. Spawns back into a regular
    koopa if alone long enough. Mario can kick it to turn it into a deadly projectile"""
    def __init__(self, level, original_velocity):
        self.shell_animation = level.asset_manager.character_atlas.load_animation("shell_green")
        self.level = level

        super().__init__(self.shell_animation.rect)

        self.respawn_timer = StunnedKoopaTroopa.RESPAWN_DELAY
        self.collider = Collider.from_entity(self, level.collider_manager, constants.Mario)
        self.collider.on_collision = self._kick_shell
        self.original_velocity = original_velocity  # so respawn can continue in original direction

        # might seem odd for a stationary shell to have movement, but consider these cases:
        #   the block/entity the shell is on disappears/moves
        #   mario has stomped a koopa in mid-air as it fell
        self.movement = SimpleMovement(self, level.collider_manager, CharacterParameters(
            max_horizontal_velocity=0.,
            max_vertical_velocity=koopa_parameters.max_vertical_velocity,
            gravity=koopa_parameters.gravity,
            jump_velocity=0.,
            squash_bounce_velocity=0.
        ), constants.Block | constants.Mario, on_collision_callback=self._kick_shell)

        self.movement.velocity = make_vector(0., 0.)

    def update(self, dt, view_rect):
        self.respawn_timer -= dt

        self.movement.update(dt)

        if self.respawn_timer <= 0.:
            self.respawn()

        if self.respawn_timer < StunnedKoopaTroopa.WARNING_ANIMATION:
            self.shell_animation.update(dt)

    def respawn(self):
        koopa = KoopaTroopa(self.level)
        koopa.position = get_aligned_foot_position(self.rect, koopa.rect)
        koopa.movement.velocity = make_vector(self.original_velocity.x, 0.)  # original koopa might've been falling
        self.level.entity_manager.register(koopa)

        self.destroy()

    def draw(self, screen, view_rect):
        screen.blit(self.shell_animation.image, world_to_screen(self.position, view_rect))

    def destroy(self):
        self.level.entity_manager.unregister(self)

    def _kick_shell(self, collision):
        if collision.hit_block:
            return

        print("kicked")

        mario = self.level.mario

        # kick shell
        shell = Shell(self.level, self.position.x - mario.position.x)
        shell.position = get_aligned_foot_position(self.rect, shell.rect)

        self.level.entity_manager.register(shell)

        mario.bounce(koopa_parameters.squash_bounce_velocity)
        self.destroy()

    @property
    def layer(self):
        return constants.Active


LevelEntity.create_generic_factory(KoopaTroopa)
