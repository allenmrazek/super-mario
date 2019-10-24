import os
import pygame
from pygame import Rect, PixelArray
from tools.TileExtractor.tile import Tile, Classification
import config


def is_exact_match_to_anchor(tile_anchor, target_surface, target_pixels: PixelArray, target_rect: Rect, trans_color):
    anchor_size = tile_anchor.surface.get_rect().size
    matches = 0

    with PixelArray(tile_anchor.surface) as anchor_pixels:
        for yanchor in range(anchor_size[1]):
            for xanchor in range(anchor_size[0]):
                try:
                    anchor_pixel = anchor_pixels[xanchor, yanchor]
                    target_pixel = target_pixels[target_rect.x + xanchor, target_rect.y + yanchor]
                except IndexError:
                    continue

                anchor_color = tile_anchor.surface.unmap_rgb(anchor_pixel)
                target_color = target_surface.unmap_rgb(target_pixel)

                if anchor_color == config.transparent_color and target_color == trans_color:
                    continue  # transparent pixels don't need to match, they just need to both be transparent

                if anchor_pixel != target_pixel:
                    return False

                matches += 1

    return matches > 0


class TileIdentifier:
    def __init__(self, target_file, world_trans_color, guess_anchor=None):
        if not os.path.exists(target_file) or not os.path.isfile(target_file):
            raise FileNotFoundError

        if isinstance(world_trans_color, tuple):
            world_trans_color = pygame.Color(*world_trans_color)

        self.world = pygame.image.load(target_file).convert(24)
        self.world_trans_color = world_trans_color

        if self.world_trans_color is None:
            # try to guess color using upper-left pixel, which is usually background
            self.world_trans_color = self.world.get_at((0, 0))
            print("guessed that world transparent color is ", self.world_trans_color)

        self.known_tiles = []

        # load all known tiles: anything that matches these hashcodes need not be re-classified
        self.known_tiles.extend(
            self._load_tiles_from("../../images/atlas_background_blocks/", Classification.Background))

        self.known_tiles.extend(
            self._load_tiles_from("../../images/atlas_solid_blocks/", Classification.SolidNoninteractive))

        self.known_tiles.extend(
            self._load_tiles_from("../../images/atlas_interactive_blocks/", Classification.SolidInteractive))

        self.known_tiles.extend(
            self._load_tiles_from("../../images/atlas_ignored_blocks/", Classification.Ignore))

        self.anchor_position = self._find_anchor(self.world, guess_anchor)
        tile_width, tile_height = self.known_tiles[0].surface.get_rect().size if len(self.known_tiles) > 0 else (16, 16)
        self.startx, self.starty = self.anchor_position[0] % tile_width, self.anchor_position[1] % tile_height

        if self.anchor_position is not None:
            self._finished = False
            self.search_rect = pygame.Rect(self.startx, self.starty, tile_width, tile_height)
        else:
            self._finished = True
            print("anchor was not found")

    @property
    def finished(self):
        if self.search_rect is not None:
            r = self.world.get_rect()

            if self.search_rect.bottom >= r.bottom or self.search_rect.right >= r.right:
                return True

        return self._finished

    @staticmethod
    def is_transparent(surface, pixels, rect, world_transparent):
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                try:
                    if surface.unmap_rgb(pixels[x, y]) != world_transparent:
                        return False
                except IndexError:
                    continue

        return True

    def locate_next(self):
        movement = self.known_tiles[0].surface.get_rect().size if len(self.known_tiles) > 0 else (16, 16)

        print("identifying next tile to classify ...")

        # find next tile to classify
        with PixelArray(self.world) as pixels:
            while self.search_rect.bottom < self.world.get_height():
                print(f"searching along {self.search_rect.top}-{self.search_rect.bottom}")

                while self.search_rect.right < self.world.get_width() \
                        and self.search_rect.bottom < self.world.get_height():
                    exists = False

                    # check for all transparent
                    if not TileIdentifier.is_transparent(self.world, pixels, self.search_rect, self.world_trans_color):

                        # otherwise, see if we recognize the tile
                        for known in self.known_tiles:
                            if not exists and is_exact_match_to_anchor(known, self.world, pixels,
                                                                       self.search_rect, self.world_trans_color):
                                exists = True

                        if not exists:
                            return

                    # else, continue
                    self.search_rect.move_ip(movement[0], 0)

                    if self.search_rect.right > self.world.get_width():
                        self.search_rect.left = self.startx
                        self.search_rect.move_ip(0, movement[1])

                self.search_rect.left = self.startx
                self.search_rect.move_ip(0, movement[1])

        self._finished = True

    def set_search_rect(self, rect):
        self.search_rect = rect

    def set_classification(self, classification):
        # classify selected tile as given arg
        tile = Tile.create_from_surface(self.world, self.search_rect, self.world_trans_color, classification)
        tile.classification = classification

        self.known_tiles.append(tile)

    def draw(self, screen):
        draw_rect = self.world.get_rect()
        draw_rect.x, draw_rect.y = -self.search_rect.x, -self.search_rect.y

        screen.blit(self.world, draw_rect)

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, self.search_rect.width, self.search_rect.height), 3)

    @staticmethod
    def _load_tiles_from(dir_path, classification):
        return [Tile.load_from_file(os.path.join(dir_path, png_name), classification) for
                png_name in [x for x in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, x))
                             and os.path.splitext(x)[1][-3:] == 'png']]

    def _find_anchor(self, surface, guess_anchor):
        # load all known anchors: these are used to identify the grid blocks are positioned on
        anchors = TileIdentifier._load_tiles_from("../../images/editor/anchors/", Classification.NotClassified)

        # we'll extend known anchors with all other known tiles as well, since calculating hash is expensive while
        # comparing them is not
        anchors.extend(self.known_tiles)

        search_rect = anchors[0].surface.get_rect()
        sr = surface.get_rect()

        if guess_anchor is not None:
            search_rect.x, search_rect.y = guess_anchor
            sr.left, sr.top = guess_anchor
            sr.width -= guess_anchor[0]
            sr.height -= guess_anchor[1]

        # advance through surface, looking for any matches to anchor hashes
        search_hash = 0

        print("searching for anchor ...")

        with pygame.PixelArray(surface) as search_pixels:
            for x in range(sr.left, sr.right - search_rect.width + 1):

                print("searching along columns at x = ", x)

                for y in range(sr.top, sr.bottom - search_rect.height + 1):
                    search_rect.x, search_rect.y = x, y

                    for known in anchors:
                        # don't use background blocks to identify anchors; they seem to not always
                        # align to a regular grid
                        if known.classification != Classification.Background and \
                                is_exact_match_to_anchor(known, self.world, search_pixels,
                                                    search_rect, self.world_trans_color) \
                                and not self.is_transparent(surface, search_pixels, search_rect, self.world_trans_color):
                            print("anchor found at ", x, ", ", y)
                            return x, y

            print("*** no anchor found ***")
            return None
