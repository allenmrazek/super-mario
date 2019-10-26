from .editor_mode import EditorMode


class ConfigMode(EditorMode):
    def __init__(self):
        super().__init__()

    def draw(self, screen):
        pass

    def on_map_click(self, evt, screen_mouse_pos):
        pass

    def on_map_mousedown(self, evt, screen_mouse_pos):
        pass

