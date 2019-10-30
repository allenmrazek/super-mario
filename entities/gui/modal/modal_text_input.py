from state.game_state import GameState
from event.game_events import GameEvents, EventHandler
from state.game_state import state_stack
from util import make_vector
from assets.gui_helper import *
import config
from event import TextInputHandler


class ModalTextInput(GameState, EventHandler):
    SIZE = 380, 128

    """This is kind of a lazy way of going about this, but we can avoid dealing with control focus
    and other things that the simple gui the game uses wasn't really designed to do"""
    def __init__(self, gui_atlas, title, on_ok_callback, on_cancel_callback, input_text=""):
        # create own instance of game events: this way, events that aren't used by this modal dialog
        # will just vanish rather than trickle down into other listeners
        game_events = GameEvents()

        super().__init__(game_events)

        font = pygame.sysfont.SysFont(None, 24)
        size = ModalTextInput.SIZE

        self.on_ok = on_ok_callback
        self.on_cancel = on_cancel_callback

        # center dialog
        pos = make_vector(config.screen_rect.centerx - size[0] // 2, config.screen_rect.centery - size[1] // 2)

        self.dialog = create_dialog(gui_atlas, pos, size, title, font)

        self.darken_surface = pygame.Surface(config.screen_rect.size)
        self.darken_surface.fill((0, 0, 0))
        self.darken_surface = self.darken_surface.convert(pygame.display.get_surface())
        self.darken_surface.set_alpha(175)

        frame_width = 20
        usable_width = self.dialog.width - 2 * frame_width
        width_per_button = usable_width // 2
        button_size = (usable_width // 2, 20)
        text_color = (0, 0, 0)
        y_pos = self.dialog.height - button_size[1] - frame_width

        self.button_ok = create_button(gui_atlas, make_vector(frame_width, y_pos),
                                       button_size, "OK", text_color=text_color, on_click_callback=self._ok)
        self.dialog.add_child(self.button_ok)

        self.button_cancel = create_button(
            gui_atlas, make_vector(self.dialog.width - width_per_button - frame_width,
                                   y_pos), button_size, "Cancel", text_color=text_color, on_click_callback=self._cancel)
        self.dialog.add_child(self.button_cancel)

        # actual text
        # create a nice background to put it on
        self.text_background = Window(make_vector(frame_width, self.dialog.get_title_bar_bottom() + 10),
                                      (size[0] - frame_width * 2, 30),
                                      gui_atlas.load_sliced("button_bkg_white"), draggable=False)
        self.dialog.add_child(self.text_background)

        self.text = Text(make_vector(8, 8), "", font, text_color, Anchor.TOP_LEFT, True)
        self.text_background.add_child(self.text)

        self.dialog.layout()

        # state
        self._finished = False
        self.input_handler = TextInputHandler(input_text)

    def update(self, dt):
        self.dialog.update(dt, None)
        self.text.text = self.input_handler.string

    def draw(self, screen):
        screen.fill((0, 0, 0))

        next_state = state_stack.get_next(self)  # type: GameState

        if next_state is not None:
            next_state.draw(screen)
            screen.blit(self.darken_surface, (0, 0))

        self.dialog.draw(screen, None)

    def activated(self):
        self.game_events.register(self)
        self.game_events.register(self.dialog)
        self.game_events.register(self.input_handler)

    def deactivated(self):
        self.game_events.unregister(self)
        self.game_events.unregister(self.dialog)
        self.game_events.unregister(self.input_handler)

    @property
    def finished(self):
        return self._finished

    def _ok(self):
        self._finished = True

        if self.on_ok:
            self.on_ok(self.input_handler.string)

    def _cancel(self):
        self._finished = True

        if self.on_cancel:
            self.on_cancel()

    def handle_event(self, evt, game_events):
        if not self.is_consumed(evt):
            if evt.type == pygame.KEYDOWN:

                if evt.key == pygame.K_ESCAPE:
                    self._cancel()
                    self.consume(evt)

                elif evt.key == pygame.K_RETURN or evt.key == pygame.K_KP_ENTER:
                    self._ok()
                    self.consume(evt)

    @staticmethod
    def spawn(gui_atlas, title, on_ok_callback, on_cancel_callback, initial_text=""):
        state_stack.push(ModalTextInput(gui_atlas, title, on_ok_callback, on_cancel_callback, initial_text))
