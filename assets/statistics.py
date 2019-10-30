from scoring import Labels
import constants
from pygame.mixer import Sound


class Statistics:
    def __init__(self, scoring: Labels):
        # make pep8 happy
        self._score = 0
        self._lives = 0
        self._coins = 0
        self._scoring = scoring
        self._elapsed = 0.
        self._remaining_time = 0

    def reset(self):
        # initial values
        self.score = 0
        self.lives = 3
        self.coins = 95
        self._remaining_time = constants.TIME_PER_LEVEL
        self._elapsed = 0.

        self._scoring.prep_world()
        self._scoring.prep_time()
        self._scoring.prep_lives()
        self._scoring.prep_coins()
        self._scoring.prep_points()

        print("note: coins set to 95, to demonstrate 1up on 100")

    def update(self, dt):
        self._elapsed += dt

        new_time = max(constants.TIME_PER_LEVEL - int(self._elapsed), 0)

        if new_time != self.remaining_time:
            self._remaining_time = new_time  # avoid creating new surface every update
            self._scoring.time = self.remaining_time
            self._scoring.prep_time()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, val):
        self._score = val
        self._scoring.points = val
        self._scoring.prep_points()

    @property
    def remaining_time(self):
        return self._remaining_time

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, val):
        self._coins = val


        if self.coins >= 100:
            self.lives += self.coins // 100
            self.coins = self.coins % 100

            Sound('sounds/sfx/smb_1-up.wav').play()

        self._scoring.coins = self._coins

        self._scoring.prep_coins()

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, val):
        self._lives = val
        self._scoring.lives = val
        self._scoring.prep_lives()

    def set_world(self, name):
        self._scoring.world = name
        self._scoring.prep_world()

    def reset_time(self):
        self._elapsed = 0.