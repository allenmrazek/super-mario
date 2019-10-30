import pygame
from pygame import Color
from .game_state import GameState
from event import GameEvents, EventHandler
from assets.level import Level
from state.run_session import RunSession
from .game_state import state_stack
from editor.editor_state import EditorState
from entities.entity_manager import EntityManager
from util import make_vector
import config
from scoring import Labels
from assets.statistics import Statistics


class MainMenu(GameState, EventHandler):
    def __init__(self, assets):
        super().__init__(GameEvents())

        self.assets = assets

        # create main menu
        font = pygame.font.Font(None, 48)
        self._banner = assets.gui_atlas.load_static("mm_Smb")
        self._mushroom = assets.gui_atlas.load_static("menu_mushroom")
        self._scoring = Labels()

        play_btn = font.render("1 Player Game", True, Color('white'))
        editor_btn = font.render("Level Editor", True, Color('white'))
        quit_btn = font.render("Quit", True, Color('white'))

        # state
        self._finished = False
        self._buttons = [play_btn, editor_btn, quit_btn]
        self._selected = 0

        self.level = Level(assets, EntityManager.create_default(), Statistics(self._scoring))
        self.level.load_from_path('levels/mainmenu.level')

        self.game_events.register(self)

    def update(self, dt):
        self.level.update(dt)

    def draw(self, screen):
        screen.fill(self.level.background_color)

        self.level.draw(screen)

        screen.blit(self._banner.image, make_vector(*config.screen_rect.center) -
                    make_vector(self._banner.image.get_width() // 2, self._banner.image.get_height() * 1.5))

        r = pygame.Rect(config.screen_rect.centerx, config.screen_rect.centery, 0, 0)

        for idx, btn in enumerate(self._buttons):
            r.width, r.height = btn.get_width(), btn.get_height()

            r.centerx = config.screen_rect.centerx

            screen.blit(btn, r)

            if r.collidepoint(*pygame.mouse.get_pos()):
                self._selected = idx

                if pygame.mouse.get_pressed()[0]:
                    if self._selected == 0:
                        self._on_play()
                    elif self._selected == 1:
                        self._on_editor()
                    else:
                        self._on_quit()

            if idx == self._selected:
                mr = self._mushroom.image.get_rect()
                mr.centery = r.centery
                mr.right = r.left - mr.width

                screen.blit(self._mushroom.image, mr)

                mr.left = r.right + mr.width

                screen.blit(self._mushroom.image, mr)

            r.y += r.height + 10

        self._scoring.show_labels(screen)

    def _on_play(self):
        state_stack.push(RunSession(self.assets))

    def _on_editor(self):
        state_stack.push(EditorState(self.assets))

    def _on_quit(self):
        self._finished = True

    @property
    def finished(self):
        return self._finished

    def handle_event(self, evt, game_events):
        if evt.type == pygame.QUIT or (evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE):
            self._finished = True
            self.consume(evt)

    def activated(self):
        pygame.mixer_music.stop()
