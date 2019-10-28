from abc import ABC, abstractmethod


class EditorMode(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def on_map_click(self, evt, screen_mouse_pos):
        pass

    @abstractmethod
    def on_map_mousedown(self, evt, screen_mouse_pos):
        pass

    @abstractmethod
    def draw(self, screen):
        # note: draws right after entity manager, so anything here will be under UI elements
        pass

    # todo: put grid drawing functions here
