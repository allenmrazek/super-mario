from .level_entity import LevelEntity
from util import make_vector
from .corpse import Corpse
from .spawn_block import SpawnBlock
import config
import constants
from .parameters import CharacterParameters
from util import get_aligned_foot_position


class AirCoin(Corpse):  # weird right? I know
    PARAMETERS = CharacterParameters(0., 1000,
                                     1150 * config.rescale_factor * config.rescale_factor,
                                     425 * config.rescale_factor, 0.)

    """Coin flies upwards a short ways, then disappears. Comes out of coin blocks"""
    def __init__(self, level, animation):
        super().__init__(level, animation, AirCoin.PARAMETERS, animation.duration, True)

        self.velocity = make_vector(0, -AirCoin.PARAMETERS.jump_velocity)

    @property
    def layer(self):
        return constants.Background


class CoinBlock(SpawnBlock):
    COIN_UP_PARAMETERS = CharacterParameters(0., 1000,
                                     950 * config.rescale_factor * config.rescale_factor,
                                     325 * config.rescale_factor, 0.)

    def __init__(self, level):
        self.level = level
        patlas = level.asset_manager.pickup_atlas

        self.coin_up = patlas.load_animation("coin_spin")

        super().__init__(level)

    def smashed(self):
        #if not self._smashed:
        self.level.asset_manager.sounds['coin'].play()
        self._smashed = True

        self.animation = self.empty
        self.level.stats.score += constants.COIN_POINT_VALUE
        self.level.stats.coins += 1

        air_coin = AirCoin(self.level, self.coin_up)
        air_coin.position = get_aligned_foot_position(self.rect, air_coin.rect)

        self.level.entity_manager.register(air_coin)

        #else:
            #self.level.asset_manager.sounds['bump'].play()

    def create_preview(self):
        block = super().create_preview()
        block.blit(self.coin_up.image, (0, 0))

        return block


LevelEntity.create_generic_factory(CoinBlock)

# def make_coin_block(level, values):
#     coin_block = CoinBlock(level, make_vector(0, 0))
#
#     if values is not None:
#         coin_block.deserialize(values)
#
#     return coin_block
#
#
# LevelEntity.register_factory(CoinBlock, make_coin_block)
