import pygame
from .game_state import GameState
from scoring import Labels
import config
from util import make_vector, copy_vector


class LevelBegin(GameState):
    DURATION = .03  # todo: fix before release

    def __init__(self, assets, level, scoring_labels: Labels, mario_stats):
        super().__init__()

        self.assets = assets
        self.scoring_labels = scoring_labels
        self.mario_stats = mario_stats
        self.level = level

        def make_centered(surface):
            return make_vector(*sr.center) - make_vector(surface.get_width() // 2, surface.get_height() // 2)

        sr = config.screen_rect
        tc = pygame.Color('white')

        self.elapsed = 0
        self.world_title = Labels.font_large.render(level.title, True, tc).convert_alpha()
        self.world_title_pos = make_centered(self.world_title) - make_vector(0, 100)

        self.x = Labels.font_large.render("x", True, tc)
        self.x_pos = make_centered(self.x) + make_vector(0, 40)

        little_mario = assets.character_atlas.load_static("mario_stand_right").image

        # scale it up
        self.mario_icon = pygame.transform.scale2x(little_mario).convert()
        self.mario_pos = copy_vector(self.x_pos) - \
            make_vector(self.mario_icon.get_width() * 2, self.mario_icon.get_height() // 4)

        self.lives = Labels.font_large.render(str(mario_stats.lives), True, tc).convert_alpha()
        self.lives_pos = self.x_pos + make_vector(self.mario_icon.get_width(), 0)

    def update(self, dt):
        self.elapsed += dt

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.scoring_labels.show_labels(screen)
        screen.blit(self.world_title, self.world_title_pos)
        screen.blit(self.x, self.x_pos)
        screen.blit(self.mario_icon, self.mario_pos)
        screen.blit(self.lives, self.lives_pos)

    @property
    def finished(self):
        return self.elapsed >= LevelBegin.DURATION

    def activated(self):
        pygame.mixer_music.stop()

    def deactivated(self):
        # pygame.mixer_music.load("sounds/music/01-main-theme-overworld.ogg")
        # pygame.mixer_music.play(-1)

        self.level.begin()

        #print("playing theme music")
