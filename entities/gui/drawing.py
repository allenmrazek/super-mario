import pygame
from .sliced_image import SlicedImage
from animation import Animation
from .container import Container
from util import make_vector

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
    # elif isinstance(source, Container):
    #     assert src_rect is not None  # is content rect
    #
    #     source.offset = make_vector(*src_rect.topleft)
    #     source.draw(target, dest_rect)

        # store current offset
        # current_offset = source.offset
        #
        # if isinstance(dest_rect, pygame.Vector2) or isinstance(dest_rect, tuple):
        #     source.offset = make_vector(*dest_rect)
        # elif isinstance(dest_rect, pygame.Rect):
        #     source.offset = make_vector(*dest_rect.topleft)
        # else:
        #     raise NotImplementedError
        #
        # source.draw(target, None)
        # source.offset = current_offset
    else:
        raise NotImplementedError


def generated_selected_version_circle(surf, clr):
    assert isinstance(surf, pygame.Surface)

    hl_surf = surf.copy().convert_alpha(pygame.display.get_surface())

    pygame.draw.circle(hl_surf, clr, hl_surf.get_rect().center, hl_surf.get_width() // 2)

    hl_surf.blit(surf, (0, 0))

    return hl_surf


def generated_selected_version_darken(surf, color_multiplier):
    assert isinstance(surf, pygame.Surface)

    hl_surf = surf.copy()

    with pygame.PixelArray(hl_surf) as pixels:
        for y in range(hl_surf.get_height()):
            for x in range(hl_surf.get_width()):
                unmapped = hl_surf.unmap_rgb(pixels[x, y])  # type: pygame.Color

                if unmapped != pygame.Color('magenta'):
                    unmapped.r = int(unmapped.r * color_multiplier)
                    unmapped.g = int(unmapped.g * color_multiplier)
                    unmapped.b = int(unmapped.b * color_multiplier)

                    pixels[x, y] = hl_surf.map_rgb(unmapped)

    return hl_surf
