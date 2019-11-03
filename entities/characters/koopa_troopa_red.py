from .koopa_troopa import KoopaTroopa, StunnedKoopaTroopa
from entities.characters.level_entity import LevelEntity
from entities.characters import Corpse
from . import CharacterParameters
from util import mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from util import get_aligned_foot_position
from .behaviors.smart_enemy_ground_movement import SmartEnemyGroundMovement

# todo: tweak movement characteristics
koopa_red_parameters = CharacterParameters(30, mstpvv('04800'), mstpva('00300'), 100, mstpvv('04200'))


class KoopaTroopaRed(KoopaTroopa):
    PATROL_RANGE = 300.

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

        self.destroy()

    def die(self):
        self.destroy()

        corpse = Corpse.create_ghost_corpse_from_entity(
            self, self.level.asset_manager.character_atlas.load_animation("shell_red"),
            self.level, 5., Corpse.STANDARD)

        self.level.entity_manager.register(corpse)
        self.level.asset_manager.sounds['stomp'].play()


class StunnedKoopaTroopaRed(StunnedKoopaTroopa):
    def __init__(self, level, original_velocity):
        super().__init__(level, original_velocity)

        self.shell_animation = level.asset_manager.character_atlas.load_animation("shell_red")


LevelEntity.create_generic_factory(KoopaTroopaRed)
