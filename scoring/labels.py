import pygame
import pygame.font


class Labels:
    font = None
    font_small = None
    font_large = None

    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)

        self.world = '1-1'

        font_name = "scoring/super_mario_font.ttf"

        Labels.font = pygame.font.Font(font_name, 22)
        Labels.font_small = pygame.font.Font(font_name, 12)
        Labels.font_large = pygame.font.Font(font_name, 30)

        self.time = 400
        self.coins = 0
        self.lives = 3
        self.points = 0

        # Declared here to get rid of warnings
        self.text1_image = None
        self.text1_rect = None
        self.text2_image = None
        self.text2_rect = None
        self.text3_image = None
        self.text3_rect = None
        self.text4_image = None
        self.text4_rect = None
        self.text5_image = None
        self.text5_rect = None
        self.points_image = None
        self.points_rect = None
        self.time_image = None
        self.time_rect = None
        self.world_image = None
        self.world_rect = None
        self.coins_image = None
        self.coins_rect = None
        self.lives_image = None
        self.lives_rect = None

        # Prep it all
        self.prep_labels()
        self.prep_lives()
        self.prep_coins()
        self.prep_world()
        self.prep_points()
        self.prep_time()

    def prep_labels(self):
        text1 = "SCORE"
        self.text1_image = self.font.render(text1, True, self.text_color, self.bg_color)
        self.text1_rect = self.text1_image.get_rect()
        self.text1_rect.left = self.text1_rect.left + 50
        self.text1_rect.top = 25

        text2 = "TIME"
        self.text2_image = self.font.render(text2, True, self.text_color, self.bg_color)
        self.text2_rect = self.text2_image.get_rect()
        self.text2_rect.left = self.text2_rect.left + 250
        self.text2_rect.top = 25

        text3 = "WORLD"
        self.text3_image = self.font.render(text3, True, self.text_color, self.bg_color)
        self.text3_rect = self.text3_image.get_rect()
        self.text3_rect.left = self.text3_rect.left + 475
        self.text3_rect.top = 25

        text4 = "COINS"
        self.text4_image = self.font.render(text4, True, self.text_color, self.bg_color)
        self.text4_rect = self.text4_image.get_rect()
        self.text4_rect.left = self.text4_rect.left + 675
        self.text4_rect.top = 25

        text5 = "LIVES"
        self.text5_image = self.font.render(text5, True, self.text_color, self.bg_color)
        self.text5_rect = self.text5_image.get_rect()
        self.text5_rect.left = self.text5_rect.left + 875
        self.text5_rect.top = 25

    def prep_points(self):
        self.points_image = self.font.render(str(self.points), True, self.text_color, self.bg_color)
        self.points_rect = self.points_image.get_rect()
        self.points_rect.left = self.points_rect.left + 50
        self.points_rect.top = 48

    def prep_time(self):
        self.time_image = self.font.render(str(self.time), True, self.text_color, self.bg_color)
        self.time_rect = self.time_image.get_rect()
        self.time_rect.left = self.time_rect.left + 260
        self.time_rect.top = 48

    def prep_world(self):
        self.world_image = self.font.render(self.world, True, self.text_color, self.bg_color)
        self.world_rect = self.world_image.get_rect()
        self.world_rect.left = self.world_rect.left + 495
        self.world_rect.top = 48

    def prep_coins(self):
        self.coins_image = self.font.render(str(self.coins), True, self.text_color, self.bg_color)
        self.coins_rect = self.coins_image.get_rect()
        self.coins_rect.left = self.coins_rect.left + 715
        self.coins_rect.top = 48

    def prep_lives(self):
        self.lives_image = self.font.render(str(self.lives), True, self.text_color, self.bg_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.lives_rect.left + 915
        self.lives_rect.top = 48

    def show_labels(self, screen):
        screen.blit(self.text1_image, self.text1_rect)
        screen.blit(self.text2_image, self.text2_rect)
        screen.blit(self.text3_image, self.text3_rect)
        screen.blit(self.text4_image, self.text4_rect)
        screen.blit(self.text5_image, self.text5_rect)
        screen.blit(self.points_image, self.points_rect)
        screen.blit(self.time_image, self.time_rect)
        screen.blit(self.world_image, self.world_rect)
        screen.blit(self.coins_image, self.coins_rect)
        screen.blit(self.lives_image, self.lives_rect)
