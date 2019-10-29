from .level_entity import LevelEntity
from util import make_vector
from util import world_to_screen
from entities.entity import Layer
from .behaviors import Smashable
from entities.entity import Entity
from .corpse import Corpse
import config


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
        return Layer.Background


class CoinBlock(LevelEntity):
    def __init__(self, level, position):
        self.level = level

        iatlas = level.asset_manager.interactive_atlas
        patlas = level.asset_manager.pickup_atlas

        self.animation = iatlas.load_animation("coin_block_ow")
        self.empty = iatlas.load_static("coin_block_empty_ow")
        self.coin_up = patlas.load_animation("coin_spin")

        super().__init__(self.empty.get_rect())

        self.position = position

        # note: Smashable assumes we're passing in UNSCALED values, so don't use our own rect size
        self.smashable = Smashable(level, self, self._on_smashed)

        self._smashed = False

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.smashable.update(dt)
        self.animation.update(dt)
        
    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))
        self.smashable.draw(screen, view_rect)

    def _on_smashed(self):
        if not self._smashed:
            self.level.asset_manager.sounds['coin'].play()
            self._smashed = True

            self.animation = self.empty

            air_coin = AirCoin(self.level, self.coin_up, self.position, AirCoin.VELOCITY)

            self.level.entity_manager.register(air_coin)
        else:
            self.level.asset_manager.sounds['bump'].play()

    def destroy(self):
        self.level.entity_manager.unregister(self)

    def create_preview(self):
        return self.animation.image.copy()

    @property
    def layer(self):
        return Layer.Block


def make_coin_block(level, values):
    coin_block = CoinBlock(level, make_vector(0, 0))

    if values is not None:
        coin_block.deserialize(values)

    return coin_block


LevelEntity.register_factory(CoinBlock, make_coin_block)
