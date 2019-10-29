from .level_entity import LevelEntity
from util import make_vector
from util import world_to_screen
from entities.entity import Layer
from .behaviors import Smashable


class CoinBlock(LevelEntity):
    def __init__(self, level, position):
        self.level = level
        self.animation = level.asset_manager.interactive_atlas.load_animation("coin_block_ow")
        self.empty = level.asset_manager.interactive_atlas.load_static("coin_block_empty_ow")
        # todo: coin flying up

        super().__init__(self.empty.get_rect())

        self.position = position

        # note: Smashable assumes we're passing in UNSCALED values, so don't use our own rect size
        self.smashable = Smashable(level, self, self._on_smashed)

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.smashable.update(dt)

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))
        self.smashable.draw(screen, view_rect)

    def _on_smashed(self):
        # todo: mario gets a coin

        mario = self.level.mario
        self.level.asset_manager.sounds['coin'].play()
        self.smashable.on_head_smash = None

        self.animation = self.empty

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
