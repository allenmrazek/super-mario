import pygame
import config


class SlicedImage:
    def __init__(self, base_surface, corner_dimensions=None):
        assert base_surface is not None

        self._base_surface = base_surface

        base_size = self._base_surface.get_rect().size

        self.corner_dimensions = corner_dimensions or (base_size[0] // 3, base_size[1] // 3)
        self._base_surface.set_colorkey(config.transparent_color)

        self._slices = self._create_slices()  # type: list
        self._generated = None
        self._generated_rect = None

    def draw(self, screen, rect):
        if self._generated is None or \
                (self._generated_rect.width != rect.width or self._generated_rect.height != rect.height):
            self._construct_surface(rect)

        screen.blit(self._generated, rect)

    def get_rect(self):
        return self._base_surface.get_rect()

    @staticmethod
    def _slice(surface: pygame.Surface, r):
        assert surface is not None

        sliced = surface.subsurface(r)

        if surface.get_colorkey() is not None:
            sliced.set_colorkey(surface.get_colorkey())

        return sliced

    def _tile(self, start, stop, src_surface, other_coord, tf_horizontal):
        draw_rect = pygame.Rect(src_surface.get_rect())
        area_rect = draw_rect.copy()

        if tf_horizontal:
            draw_rect.y = other_coord
        else:
            draw_rect.x = other_coord

        step_size = src_surface.get_width() if tf_horizontal else src_surface.get_height()

        for counting_coord in range(start, stop, step_size):
            if tf_horizontal:
                draw_rect.x = counting_coord
                draw_rect.width = min(stop - counting_coord, src_surface.get_width())
                area_rect.width = draw_rect.width
            else:
                draw_rect.y = counting_coord
                draw_rect.height = min(stop - counting_coord, src_surface.get_height())
                area_rect.width = draw_rect.height

            self._generated.blit(src_surface, draw_rect, area_rect)

    def _construct_surface(self, rect):
        # for now, just don't allow sizes that are too small
        if rect.width < 2 * self.corner_dimensions[0] or rect.height < 2 * self.corner_dimensions[1]:
            self._generated = pygame.Surface(rect.size).convert()
            self._generated_rect = self._generated.get_rect()
            self._generated.fill(config.transparent_color)  # no color key: make it stand out
            return

        assert rect.width >= 2 * self.corner_dimensions[0]
        assert rect.height >= 2 * self.corner_dimensions[1]

        self._generated = pygame.Surface(rect.size).convert(24)  # note: assumes 24 bit surfaces (no per-pixel alpha)
        self._generated_rect = self._generated.get_rect()

        # expand center tile
        scale_x = float(self._generated_rect.width - 2 * self.corner_dimensions[0]) / self.corner_dimensions[0]
        scale_y = float(self._generated_rect.height - 2 * self.corner_dimensions[1]) / self.corner_dimensions[1]
        center_slice = self._slices[4]
        scale_center = int(center_slice.get_width() * scale_x), int(center_slice.get_height() * scale_y)

        center = pygame.transform.smoothscale(self._slices[4], scale_center)

        r = center.get_rect()
        r.center = self._generated_rect.center
        self._generated.blit(center, r)

        if center_slice.get_colorkey() is not None:
            self._generated.set_colorkey(center_slice.get_colorkey())

        # corners of image
        corner_rect = pygame.Rect(0, 0, *self.corner_dimensions)
        self._generated.blit(self._slices[0], corner_rect)
        corner_rect.right = self._generated_rect.right
        self._generated.blit(self._slices[2], corner_rect)
        corner_rect.bottom = self._generated_rect.bottom
        self._generated.blit(self._slices[8], corner_rect)
        corner_rect.left = 0
        self._generated.blit(self._slices[6], corner_rect)

        # tile along top and bottom of image
        start_x = self.corner_dimensions[0]
        stop_x = self._generated_rect.width - self.corner_dimensions[0]
        start_y = self.corner_dimensions[1]
        stop_y = self._generated_rect.height - self.corner_dimensions[1]

        # top
        self._tile(start_x, stop_x, self._slices[1], 0, True)

        # bottom
        self._tile(start_x, stop_x, self._slices[7], self._generated_rect.height - self.corner_dimensions[1], True)

        # left
        self._tile(start_y, stop_y, self._slices[3], 0, False)

        # right
        self._tile(start_y, stop_y, self._slices[5], self._generated_rect.width - self.corner_dimensions[0], False)

    def _create_slices(self):
        assert self._base_surface.get_width() >= 2 * self.corner_dimensions[0]
        assert self._base_surface.get_height() >= 2 * self.corner_dimensions[1]

        # 0 1 2
        # 3 4 5
        # 6 7 8

        slices = [None for _ in range(9)]
        base_rect = self._base_surface.get_rect()

        # create corner slices (0, 2, 6, 8)
        corner_rect = pygame.Rect(0, 0, *self.corner_dimensions)

        slices[0] = SlicedImage._slice(self._base_surface, corner_rect)

        corner_rect.right = base_rect.right
        slices[2] = SlicedImage._slice(self._base_surface, corner_rect)

        corner_rect.bottom = base_rect.bottom
        slices[8] = SlicedImage._slice(self._base_surface, corner_rect)

        corner_rect.left = 0
        slices[6] = SlicedImage._slice(self._base_surface, corner_rect)

        # create middle slice
        middle_width = base_rect.width - 2 * self.corner_dimensions[0]
        middle_height = base_rect.height - 2 * self.corner_dimensions[1]
        middle_rect = pygame.Rect(self.corner_dimensions[0], self.corner_dimensions[1], middle_width, middle_height)

        slices[4] = SlicedImage._slice(self._base_surface, middle_rect)

        # now each of the four side slices which aren't corners
        side_rect = pygame.Rect(self.corner_dimensions[0], 0, *self.corner_dimensions)
        slices[1] = SlicedImage._slice(self._base_surface, side_rect)

        side_rect.bottom = base_rect.bottom
        slices[7] = SlicedImage._slice(self._base_surface, side_rect)

        side_rect.left = 0
        side_rect.top = self.corner_dimensions[1]
        side_rect.width = self.corner_dimensions[0]
        side_rect.height = self.corner_dimensions[1]

        slices[3] = SlicedImage._slice(self._base_surface, side_rect)

        side_rect.right = base_rect.right
        slices[5] = SlicedImage._slice(self._base_surface, side_rect)

        return slices
