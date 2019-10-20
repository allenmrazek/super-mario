from abc import ABC, abstractmethod
from copy import copy
import pygame


class EventHandler(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def handle_event(self, evt, game_events):
        pass

    @staticmethod
    def consume(evt):
        evt.consumed = True

    @staticmethod
    def is_consumed(evt):
        if hasattr(evt, "consumed"):
            return evt.consumed
        return False


class GameEvents:
    def __init__(self):
        self._handlers = []

    def do_events(self):
        handlers = copy(self._handlers)  # in case event handlers insert more event handlers on an event

        for evt in pygame.event.get():
            evt.consumed = False

            for handler in handlers:
                handler.handle_event(evt, self)

                if evt.consumed:
                    break

    def register(self, handler: EventHandler):
        if handler not in self._handlers:
            self._handlers.append(handler)

    def unregister(self, handler: EventHandler):
        if handler in self._handlers:
            self._handlers.remove(handler)