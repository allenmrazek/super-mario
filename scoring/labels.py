import pygame
import pygame.font

X = 1024
Y = 675


class Labels:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = (0, 0, (0, 0, 0))
        self.text_color = (255, 255, 255)
        self.initial_points = '0'
        self.font = pygame.font.Font("scoring/super_mario_font.ttf", 22)

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
        self.points_image = self.font.render(self.initial_points, True, self.text_color, self.bg_color)
        self.points_rect = self.points_image.get_rect()
        self.points_rect.left = self.points_rect.left + 100
        self.points_rect.top = 48

    def show_labels(self):
        self.screen.blit(self.text1_image, self.text1_rect)
        self.screen.blit(self.text2_image, self.text2_rect)
        self.screen.blit(self.text3_image, self.text3_rect)
        self.screen.blit(self.text4_image, self.text4_rect)
        self.screen.blit(self.text5_image, self.text5_rect)
        self.screen.blit(self.points_image, self.points_rect)
