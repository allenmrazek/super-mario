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
        self.initial_points = '000000'
        self.font = pygame.font.Font("scoring/super_mario_font.ttf", 22)

    def prep_labels(self):
        text1 = "MARIO"
        self.text1_image = self.font.render(text1, True, self.text_color, self.bg_color)
        self.text1_rect = self.text1_image.get_rect()
        self.text1_rect.left = self.text1_rect.left + 75
        self.text1_rect.top = 25

        text2 = "WORLD"
        self.text2_image = self.font.render(text2, True, self.text_color, self.bg_color)
        self.text2_rect = self.text2_image.get_rect()
        self.text2_rect.left = self.text2_rect.left + 600
        self.text2_rect.top = 25

        text3 = "TIME"
        self.text3_image = self.font.render(text3, True, self.text_color, self.bg_color)
        self.text3_rect = self.text3_image.get_rect()
        self.text3_rect.left = self.text3_rect.left + 825
        self.text3_rect.top = 25

    def prep_points(self):
        self.points_image = self.font.render(self.initial_points, True, self.text_color, self.bg_color)
        self.points_rect = self.points_image.get_rect()
        self.points_rect.left = self.points_rect.left + 75
        self.points_rect.top = 48

    def show_labels(self):
        self.screen.blit(self.text1_image, self.text1_rect)
        self.screen.blit(self.text2_image, self.text2_rect)
        self.screen.blit(self.text3_image, self.text3_rect)
        self.screen.blit(self.points_image, self.points_rect)
