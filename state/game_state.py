from abc import abstractmethod
from abc import ABC
from event import GameEvents


class GameState(ABC):
    def __init__(self, game_events=None):
        super().__init__()

        self.game_events = game_events or GameEvents()

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @property
    @abstractmethod
    def finished(self):
        return True

    def activated(self):
        """Script just became top state in stack"""
        pass

    def deactivated(self):
        pass

    def do_events(self):
        self.game_events.do_events()


class NoStatesError(RuntimeError):
    pass


class GameStateStack:
    def __init__(self, initial_state=None):
        self.states = [] if initial_state is None else [initial_state]

        if self.top is not None:
            initial_state.activated()

    @property
    def top(self):
        return self.states[-1] if len(self.states) > 0 else None

    def push(self, state):
        assert state is not None

        if self.top is not None:
            self.top.deactivated()

        self.states.append(state)
        self.top.activated()

    def pop(self):
        top = self.top

        if top is not None:
            # deactivate current top
            top.deactivated()

            old_top = self.states.pop(len(self.states) - 1)

            # get new top (if any) and let it know it just became active
            top = self.top

            if top:
                top.activated()

            return old_top
        raise NoStatesError

    def update(self, dt):
        top = self.top

        if top:
            top.update(dt)

            # one of the things that might've happened is the top state switched ... so don't use top here, use
            # self.top
            if self.top.finished:
                self.pop()

    def draw(self, screen):
        top = self.top
        if top:
            top.draw(screen)

    def event(self, event):
        top = self.top
        if top:
            top.event(event)

    def get_next(self, state):
        # given a state, return the next state that would run once state finishes
        idx = self.states.index(state)

        if idx > 0:
            return self.states[idx - 1]
        return None


state_stack = GameStateStack()
