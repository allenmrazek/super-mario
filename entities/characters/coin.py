from .behaviors import Interactive
from .level_entity import LevelEntity
from entities.entity import Layer
from util import make_vector, world_to_screen
from scoring import labels


class Coin(LevelEntity):
    def __init__(self, level):
        self.level = level

        pickup_atlas = level.asset_manager.pickup_atlas

        self.animation = pickup_atlas.load_animation("coin_world")

        super().__init__(self.animation.rect)

        self.interactive = Interactive(level, self, (4, 2), (8, 12), self._on_collected)
        self.collect_sound = level.asset_manager.sounds['coin']

    def update(self, dt, view_rect):
        self.interactive.update(dt)
        self.animation.update(dt)

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))
        self.interactive.draw(screen, view_rect)

    def destroy(self):
        super().destroy()

        self.level.entity_manager.unregister(self)

    def _on_collected(self, collision):
        labels.Labels.coins += 1
        labels.Labels.points += 200
        self.collect_sound.play()

        self.destroy()

    def create_preview(self):
        return self.animation.frames[0].copy()

    @property
    def layer(self):
        return Layer.Active


def make_coin(level, values):
    coin = Coin(level)

    if values is not None:
        coin.deserialize(values)

    return coin


LevelEntity.register_factory(Coin, make_coin)
