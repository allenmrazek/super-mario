from .level_entity import LevelEntity
from util import make_vector
from util import world_to_screen
from .behaviors import Smashable
from entities.entity import Entity
from .corpse import Corpse
from .spawn_block import SpawnBlock
import config
import constants


class AirCoin(Corpse):  # weird right? I know
    VELOCITY = 325 * config.rescale_factor
    GRAVITY = 950 * config.rescale_factor * config.rescale_factor

    """Coin flies upwards a short ways, then disappears. Comes out of coin blocks"""
    def __init__(self, level, animation, position, upwards_velocity):
        super().__init__(level, animation, animation.duration, position)

        self.velocity = -upwards_velocity

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.velocity += AirCoin.GRAVITY * dt
        self.position = self.position + make_vector(0, self.velocity * dt)

    @property
    def layer(self):
        return constants.Background


class CoinBlock(SpawnBlock):
    def __init__(self, level, position):
        self.level = level
        patlas = level.asset_manager.pickup_atlas

        self.coin_up = patlas.load_animation("coin_spin")

        super().__init__(level, position)

        self.position = position

    def smashed(self):
        if not self._smashed:
            self.level.asset_manager.sounds['coin'].play()
            self._smashed = True

            self.animation = self.empty
            self.level.stats.score += constants.COIN_POINT_VALUE
            self.level.stats.coins += 1

            air_coin = AirCoin(self.level, self.coin_up, self.position, AirCoin.VELOCITY)

            self.level.entity_manager.register(air_coin)

        else:
            self.level.asset_manager.sounds['bump'].play()

    def create_preview(self):
        block = super().create_preview()
        block.blit(self.coin_up.image, (0, 0))

        return block


def make_coin_block(level, values):
    coin_block = CoinBlock(level, make_vector(0, 0))

    if values is not None:
        coin_block.deserialize(values)

    return coin_block


LevelEntity.register_factory(CoinBlock, make_coin_block)
