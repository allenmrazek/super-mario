import pygame


def calc_hash(surface, pixels, rect: pygame.Rect, trans_color):
    """trans_color, which might be set from the surface being scanned, is to be ignored in calculating hash value"""
    val = 0
    counter = 0

    for y in range(rect.height):
        for x in range(rect.width):
            int_pixel = pixels[rect.left + x, rect.top + y]

            if surface.unmap_rgb(int_pixel) != trans_color:
                val ^= int_pixel
                counter += 1

    return val, counter


