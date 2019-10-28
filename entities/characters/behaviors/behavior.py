from abc import ABC, abstractmethod


class Behavior(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen, view_rect):
        pass

    @abstractmethod
    def destroy(self):
        pass
