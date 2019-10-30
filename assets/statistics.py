from scoring import Labels


class Statistics:
    INITIAL_TIME = 400

    def __init__(self, scoring: Labels):
        # make pep8 happy
        self._score = 0
        self._lives = 0
        self._coins = 0
        self._time_left = 0
        self._scoring = scoring
        self.reset()

    def reset(self):
        # initial values
        self.score = 0
        self.lives = 3
        self.coins = 0
        self.remaining_time = Statistics.INITIAL_TIME

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
        return self._time_left

    @remaining_time.setter
    def remaining_time(self, val):
        self._time_left = val
        self._scoring.time = val
        self._scoring.prep_time()

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, val):
        self._coins = val
        self._scoring.coins = val
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
