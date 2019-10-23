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


def generated_selected_version(surf, clr):
    assert isinstance(surf, pygame.Surface)

    hl_surf = surf.copy().convert_alpha(pygame.display.get_surface())

    pygame.draw.circle(hl_surf, clr, hl_surf.get_rect().center, hl_surf.get_width() // 2)

    hl_surf.blit(surf, (0, 0))

    return hl_surf

    # with pygame.PixelArray(gamma_surf) as pixels:
    #
    #     for y in range(gamma_surf.get_height()):
    #         for x in range(gamma_surf.get_width()):
    #             unmapped = gamma_surf.unmap_rgb(pixels[x, y])  # type: pygame.Color
    #             clr = unmapped.hsva
    #             clr = (*clr[0:3], clr[3] * value_multiplier, clr[-1:])
    #             unmapped.hsva = clr
    #             pixels[x, y] = gamma_surf.map_rgb(unmapped)
    #
    # return gamma_surf
