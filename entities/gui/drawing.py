import pygame
from .sliced_image import SlicedImage
from animation import Animation


# distinguishes between a color, a Surface, and a SlicedImage
def smart_draw(target, source, dest_rect=None, src_rect=None):
    assert target is not None
    assert source is not None

    if isinstance(source, pygame.Surface):
        target.blit(source, dest_rect, src_rect)
    elif isinstance(source, pygame.Color) or isinstance(source, tuple):
        assert dest_rect is not None

        target.fill(source, dest_rect)
    elif isinstance(source, SlicedImage):
        assert dest_rect is not None

        source.draw(target, dest_rect)
    elif isinstance(source, Animation):
        assert dest_rect is not None

        target.blit(source.image, dest_rect)
    else:
        raise NotImplementedError
