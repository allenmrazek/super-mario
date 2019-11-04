from .level_entity import LevelEntity
from .spawners.spawn_block import SpawnBlock


class StarmanBlock(SpawnBlock):
    def __init__(self, level):
        super().__init__(level)

        self.star = level.asset_manager.pickup_atlas.load_animation('star')

    def smashed(self):
        self.level.asset_manager.sounds['powerup_appears'].play()
        self._smashed = True
        self.animation = self.empty

        powerup = self.create_rising_powerup()
        self.level.entity_manager.register(powerup)

    def create_preview(self):
        s = super().create_preview()
        s.blit(self.star.image, (0, 0))

        return s

    def create_starman(self, position):
        from .starman import Starman
        starman = Starman(self.level, position)
        self.level.entity_manager.register(starman)

    def create_rising_powerup(self):
        from .mushroom_block import RisingPowerup

        # if mario isn't super, this will be a mushroom. Otherwise, it's a fire flower
        patlas = self.level.asset_manager.pickup_atlas

        anim = patlas.load_animation("star")
        cb = self.create_starman

        rising = RisingPowerup(self.level, anim, cb)
        rising.position = self.position

        return rising


LevelEntity.create_generic_factory(StarmanBlock)
