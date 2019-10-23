import os
import pygame
from pygame import Rect, PixelArray
from level.tile import Tile, Classification
from level.util import calc_hash
from util import make_vector


def is_exact_match_to_anchor(tile_anchor, target_surface, target_pixels: PixelArray, target_rect: Rect, trans_color):
    anchor_size = tile_anchor.surface.get_rect().size
    matches = 0

    with PixelArray(tile_anchor.surface) as anchor_pixels:
        for yanchor in range(anchor_size[1]):
            for xanchor in range(anchor_size[0]):
                anchor_pixel = anchor_pixels[xanchor, yanchor]
                target_pixel = target_pixels[target_rect.x + xanchor, target_rect.y + yanchor]

                anchor_color = tile_anchor.surface.unmap_rgb(anchor_pixel)
                target_color = target_surface.unmap_rgb(target_pixel)

                if anchor_color == trans_color or target_color == trans_color:
                    continue  # transparent pixels on either always pass

                if anchor_pixel != target_pixel:
                    return False

                matches += 1

    return matches > 0


class TileIdentifier:
    def __init__(self, target_file, world_trans_color):
        if not os.path.exists(target_file) or not os.path.isfile(target_file):
            raise FileNotFoundError

        if isinstance(world_trans_color, tuple):
            world_trans_color = pygame.Color(*world_trans_color)

        self.world = pygame.image.load(target_file).convert(32)
        self.world_trans_color = world_trans_color

        self.known_tiles = []

        # load all known tiles: anything that matches these hashcodes need not be re-classified
        self.known_tiles.extend(
            self._load_tiles_from("../../images/atlas_background_blocks/", Classification.Background))

        self.known_tiles.extend(
            self._load_tiles_from("../../images/atlas_solid_blocks/", Classification.SolidNoninteractive))

        self.known_tiles.extend(
            self._load_tiles_from("../../images/atlas_interactive_blocks/", Classification.SolidInteractive))

        self.anchor_position = self._find_anchor(self.world, self.world_trans_color)
        tile_width, tile_height = self.known_tiles[0].surface.get_rect().size
        self.startx, self.starty = self.anchor_position[0] % tile_width, self.anchor_position[1] % tile_height

        if self.anchor_position is not None:
            self._finished = False
            self.search_rect = pygame.Rect(self.startx, self.starty, tile_width, tile_height)
        else:
            self._finished = True
            print("anchor was not found")

    @property
    def finished(self):
        return self._finished

    def locate_next(self):
        # find next tile to classify
        with PixelArray(self.world) as pixels:
            while self.search_rect.bottom <= self.world.get_height():
                while self.search_rect.right <= self.world.get_width():
                    hashcode = calc_hash(self.world, pixels, self.search_rect, self.world_trans_color)

                    # does this hash match any known tiles?
                    matches = [t for t in self.known_tiles if t.hashcode == hashcode[0] and is_exact_match_to_anchor(
                        t, self.world, pixels, self.search_rect, self.world_trans_color
                    )]

                    if not any(matches) and hashcode[1] > 0:
                        print("found hashcode ", hashcode[0])
                        return

                    # else, continue
                    self.search_rect.move_ip(self.known_tiles[0].surface.get_width(), 0)
                    if self.search_rect.right > self.world.get_width():
                        self.search_rect.left = self.startx
                        self.search_rect.move_ip(0, self.known_tiles[0].surface.get_height())

        self._finished = True

    def set_search_rect(self, rect):
        self.search_rect = rect

    def set_classification(self, classification):
        # classify selected tile as given arg
        tile = Tile.create_from_surface(self.world, self.search_rect, self.world_trans_color)
        tile.classication = classification

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

    def _find_anchor(self, surface, trans_color):
        # load all known anchors: these are used to identify the grid blocks are positioned on
        anchors = TileIdentifier._load_tiles_from("../../images/editor/anchors/", Classification.NotClassified)

        # we'll extend known anchors with all other known tiles as well, since calculating hash is expensive while
        # comparing them is not
        anchors.extend(self.known_tiles)

        search_rect = anchors[0].surface.get_rect()
        sr = surface.get_rect()

        # advance through surface, looking for any matches to anchor hashes
        search_hash = 0

        pygame.image.save(surface, "../../images/test/all_zero.png")

        with pygame.PixelArray(surface) as search_pixels:
            for x in range(sr.left, sr.right - search_rect.width + 1):
                for y in range(sr.top, sr.bottom - search_rect.height + 1):
                    search_rect.x, search_rect.y = x, y

                    search_hash = calc_hash(surface, search_pixels, search_rect, trans_color)

                    # determine if this hashcode matches any anchor(s)
                    matches = [a for a in anchors if a.hashcode == search_hash[0] and is_exact_match_to_anchor(
                        a, surface, search_pixels, search_rect, trans_color
                    )]

                    if any(matches) and search_hash[1] > 0:
                        return x, y

            return None
