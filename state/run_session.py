import pygame
from .game_state import GameState
from assets.statistics import Statistics
from assets.level import Level
from entities.entity_manager import EntityManager
from .run_level import RunLevel
from state.game_state import state_stack
from scoring import Labels
from event import EventHandler
from .level_begin import LevelBegin


class RunSession(GameState, EventHandler):
    """A session persists between levels, and is mainly about keep tracking of score, lives. A session ends
    when the player has run out of lives or has beaten all levels"""
    def __init__(self, assets):
        super().__init__()

        assert assets is not None

        self._finished = False
        self.assets = assets
        self.scoring_labels = Labels()
        self.mario_stats = Statistics(self.scoring_labels)

        self.levels = ['flag1.level', 'flag2.level']
        self.current_level = None
        self.level_runner = None

    def update(self, dt):
        self.level_runner.update(dt)
        self.mario_stats.update(dt)

        if self.level_runner.finished:
            self.change_state()

    def draw(self, screen):
        self.level_runner.draw(screen)
        self.scoring_labels.show_labels(screen)

    @property
    def finished(self):
        return self._finished or self.mario_stats.lives <= 0 or not any(self.levels)

    def change_state(self):
        if self.mario_stats.lives == 0:
            # todo: game over
            print("game over message")
        else:
            # play again if didn't clear it or haven't tried yet
            self.current_level = self.current_level or Level(self.assets, EntityManager.create_default(), self.mario_stats)

            if self.current_level.cleared and len(self.levels) > 0:
                self.levels.pop(0)

            if len(self.levels) > 0:
                # load and play next level
                self.current_level.load_from_path("levels/" + self.levels[0])

                # we'll control this state ourselves rather than pushing it onto the stack, so we can draw
                # score on it
                self.level_runner = RunLevel(self.game_events, self.assets, self.current_level, self.mario_stats)

                # overlay with level begin message
                state_stack.push(LevelBegin(self.assets, self.scoring_labels, self.mario_stats))
            else:
                # todo: won the game!
                print("won the game!")
                pass

    def activated(self):
        if not self.level_runner or self.level_runner.finished:
            if self.current_level and self.current_level.cleared:
                # show clear message
                # todo: push clear message
                self.level_runner = None
            else:
                self.change_state()  # move to next state (loss, victory, or level start)
        elif self.level_runner:
            self.level_runner.activated()
            self.current_level.begin()
        else:
            # no level runner -> we either just started, or finished a clear message
            self.change_state()

        self.game_events.register(self)

    def deactivated(self):
        if self.level_runner is not None:
            self.level_runner.deactivated()

        self.game_events.unregister(self)

    def handle_event(self, evt, game_events):
        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            self._finished = True
