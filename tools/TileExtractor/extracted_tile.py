import os
import pygame


def calc_hash(src, rect: pygame.Rect):
    resource = False

    if not isinstance(src, pygame.PixelArray):
        resource = True
        src = pygame.PixelArray(src)

    val = 0

    for y in range(rect.height):
        for x in range(rect.width):
            val ^= src[rect.left + x, rect.top + y]

    if resource:
        src.close()

    return val


class ExtractedTile:
    def __init__(self, surface, hashcode):
        self.surface = surface
        self.hashcode = hashcode

    @staticmethod
    def load_from_file(path):
        if not os.path.exists(path) or not os.path.isfile(path):
            raise FileNotFoundError

        surf = pygame.image.load(path).convert_alpha(pygame.display.get_surface())

        return ExtractedTile(surf, calc_hash(surf, surf.get_rect()))
