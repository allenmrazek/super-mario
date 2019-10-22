from .game_state import GameState
from .game_state import GameStateStack
#from editor.dialogs import ToolDialog
from entities.entity import EntityManager, Layer
import config


class EditorState(GameState):
    def __init__(self, game_events):
        super().__init__(game_events)

        #self.tool_dialog = ToolDialog()

        self.entity_manager = EntityManager({Layer.Interface: set()}, [Layer.Interface])
        #self.entity_manager.register(self.tool_dialog)

    def draw(self, screen):
        screen.fill(config.default_background_color)

        self.entity_manager.draw(screen)

    def update(self, dt):
        self.entity_manager.update(dt)

    @property
    def finished(self):
        return False

    def activated(self):
        pass
        #self.game_events.register(self.tool_dialog)

    def deactivated(self):
        pass
        #self.game_events.unregister(self.tool_dialog)
