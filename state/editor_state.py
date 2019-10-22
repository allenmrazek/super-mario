from .game_state import GameState
from .game_state import GameStateStack


class EditorState(GameState):
    def __init__(self, game_events):
        super().__init__(game_events)

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    @property
    def finished(self):
        return False
