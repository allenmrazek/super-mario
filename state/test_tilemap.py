from .game_state import GameState
from tileset import TileSet
from tilemap import TileMap
import config


class TestTileMap(GameState):
    def __init__(self, input_state):
        super().__init__(input_state)

        self.tileset = TileSet("NES - Super Mario Bros - Tileset.png", 16)
        self.map = TileMap(self.tileset)

    def update(self, elapsed):
        pass

    def draw(self, screen):
        self.map.draw(screen, config.screen_rect)

    @property
    def finished(self):
        return False
