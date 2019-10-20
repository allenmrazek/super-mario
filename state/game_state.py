from abc import abstractmethod
from abc import ABC
from event.game_events import GameEvents


class GameState(ABC):
    def __init__(self, game_events):
        super().__init__()
        self.game_events = game_events

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
        """Script is no longer topmost on stack. Not called for popped states"""
        pass


class NoStatesError(RuntimeError):
    pass


class GameStateStack:
    def __init__(self, initial_state=None):
        self._states = [] if initial_state is None else [initial_state]

        if self.top is not None:
            initial_state.activated()

    @property
    def top(self):
        return self._states[0] if len(self._states) > 0 else None

    @top.setter
    def top(self, state):
        assert state is not None

        if state is not self.top and self.top is not None:
            self.top.deactivated()

        self._states.insert(0, state)
        self.top.activated()

    def push(self, state):
        assert state is not None
        self.top = state

    def pop(self):
        top = self.top

        if top is not None:
            old_top = self._states.pop(0)

            # get new top and let it know it just became active
            top = self.top
            if top:
                top.activated()

            return old_top
        raise NoStatesError

    def update(self, dt):
        top = self.top

        if top:
            top.update(dt)

            if top.finished:
                self.pop()

    def draw(self, screen):
        top = self.top

        if top:
            top.draw(screen)

    def event(self, event):
        top = self.top

        if top:
            top.event(event)
