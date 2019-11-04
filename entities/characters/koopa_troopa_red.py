from .koopa_troopa import KoopaTroopa, StunnedKoopaTroopa
from entities.characters.level_entity import LevelEntity
from entities.characters import Corpse
from . import CharacterParameters
from util import mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from util import get_aligned_foot_position
from .behaviors.smart_enemy_ground_movement import SmartEnemyGroundMovement
import config
from util import make_vector, copy_vector
from .floaty_points import FloatyPoints

# todo: tweak movement characteristics
koopa_red_parameters = CharacterParameters(30, mstpvv('04800'), mstpva('00300'), 100, mstpvv('04200'))
winged_koopa_red_parameters = CharacterParameters(30, mstpvv('04800'), mstpva('00300'), 100, mstpvv('08000'))


class KoopaTroopaRed(KoopaTroopa):
    PATROL_RANGE = 300. * config.rescale_factor

    def __init__(self, level):
        super().__init__(level)

        ca = level.asset_manager.character_atlas

        self.left_animation = ca.load_animation("koopa_red_left")
        self.right_animation = ca.load_animation("koopa_red_right")
        self.movement = SmartEnemyGroundMovement(self,
                                                 level.collider_manager,
                                                 koopa_red_parameters,
                                                 KoopaTroopaRed.PATROL_RANGE)

    def stunned(self):
        # create a "stunned" version of the koopa. It will transform back into a koopa if left alone
        stunned = StunnedKoopaTroopaRed(self.level, self.movement.velocity)
        stunned.position = get_aligned_foot_position(self.rect, stunned.rect)
        self.level.entity_manager.register(stunned)

        self.level.asset_manager.sounds['stomp'].play()
        FloatyPoints.display(self.level, KoopaTroopa.POINT_VALUE, self)
        self.destroy()

    def die(self):
        self.destroy()

        corpse = Corpse.create_ghost_corpse_from_entity(
            self, self.level.asset_manager.character_atlas.load_animation("shell_red"),
            self.level, 5., Corpse.STANDARD)

        self.level.entity_manager.register(corpse)
        self.level.asset_manager.sounds['stomp'].play()
        FloatyPoints.display(self.level, KoopaTroopa.POINT_VALUE + StunnedKoopaTroopa.POINT_VALUE, self)


class StunnedKoopaTroopaRed(StunnedKoopaTroopa):
    def __init__(self, level, original_velocity):
        super().__init__(level, original_velocity)

        self.shell_animation = level.asset_manager.character_atlas.load_animation("shell_red")


class WingedKoopaTroopaRed(KoopaTroopaRed):
    FLY_HEIGHT = config.base_tile_dimensions[1] * config.rescale_factor * 3  # 6 tiles total
    FLY_FREQUENCY = 0.25
    POINT_VALUE = 400

    def __init__(self, level):
        super().__init__(level)

        ca = level.asset_manager.character_atlas

        self.left_animation = ca.load_animation("koopa_red_winged_left")
        self.right_animation = ca.load_animation("koopa_red_winged_right")

        from .behaviors.koopa_floating import KoopaFloating
        self.movement.destroy()
        self.movement = KoopaFloating(
            level, self, WingedKoopaTroopaRed.FLY_HEIGHT, WingedKoopaTroopaRed.FLY_FREQUENCY,
            make_vector(0, 0), mstpvv('08000'), self.on_squashed,
            self._on_mario_invincible
        )

        self.squashable.on_squashed = self.on_squashed

    def update(self, dt, view_rect):
        self.active_animation.update(dt)
        super().update(dt, view_rect)

    def on_squashed(self):
        # winged koopa loses its wings
        self.destroy()

        ground = KoopaTroopaRed(self.level)

        # position it under mario (don't want them touching)
        mario = self.level.mario
        pos = self.position
        pos.y = mario.movement.get_foot_position().y
        ground.position = pos

        self.level.entity_manager.register(ground)

        self.level.asset_manager.sounds['stomp'].play()

        self.level.mario.bounce(winged_koopa_red_parameters.jump_velocity)

        FloatyPoints.display(self.level, WingedKoopaTroopaRed.POINT_VALUE, self)

    def deserialize(self, values):
        super().deserialize(values)
        self.movement.center_position = copy_vector(self.position)


LevelEntity.create_generic_factory(KoopaTroopaRed)
LevelEntity.create_generic_factory(WingedKoopaTroopaRed)