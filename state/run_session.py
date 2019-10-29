from .game_state import GameState
from assets.statistics import Statistics
from assets.level import Level
from entities.entity_manager import EntityManager
from .run_level import RunLevel
from state.game_state import state_stack


class RunSession(GameState):
    """A session persists between levels, and is mainly about keep tracking of score, lives. A session ends
    when the player has run out of lives or has beaten all levels"""
    def __init__(self, game_events, assets):
        super().__init__(game_events)

        assert assets is not None

        self.assets = assets
        self.mario_stats = Statistics()

        self.levels = ['flag1.level', 'flag2.level']
        self.current_level = None

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    @property
    def finished(self):
        return self.mario_stats.lives <= 0 or not any(self.levels)

    def activated(self):
        if self.mario_stats.lives == 0:
            # todo: game over
            print("game over message")
        else:
            # play again if didn't clear it or haven't tried yet
            self.current_level = self.current_level or Level(self.assets, EntityManager.create_default())

            if self.current_level.cleared:
                self.levels.pop(0)

            if len(self.levels) > 0:
                # load and play next level
                self.current_level.load_from_path("levels/" + self.levels[0])

                state_stack.push(RunLevel(self.game_events, self.assets, self.current_level, self.mario_stats))
            else:
                # todo: won the game!
                print("won the game!")
                pass

    def deactivated(self):
        pass
