import argparse
import os
import math
import pygame
from typing import NamedTuple
from pygame import image
from pygame import Rect
from pygame import Surface
from pygame import PixelArray


# identify tiles quickly by hash value
class _GeneratedTile(NamedTuple):
    rect: Rect
    hash_value: int

    def __hash__(self):
        return self.hash_value

    def __eq__(self, other):
        return self.hash_value == other.hash


class _Anchor(NamedTuple):
    x_position: int
    y_position: int


def calc_hash(surface_pixels: PixelArray, rect: Rect):
    val = 0

    for yy in range(rect.height):
        for xx in range(rect.width):
            val ^= surface_pixels[rect.left + xx, rect.top + yy]

    return val


def is_exact_match(surface_pixels: PixelArray, r1: Rect, r2: Rect):
    if r1.width != r2.width or r1.height != r2.height:
        return False

    # compare, pixel-by-pixel
    for yy in range(r1.height):
        for xx in range(r1.width):
            r1_pixel = surface_pixels[xx + r1.x, yy + r1.y]
            r2_pixel = surface_pixels[xx + r2.x, yy + r2.y]

            if r1_pixel != r2_pixel:
                return False

    return True


def is_exact_match_to_anchor(anchor_pixels: PixelArray, anchor_size, target_pixels: PixelArray, target_rect: Rect):
    for yanchor in range(anchor_size[1]):
        for xanchor in range(anchor_size[0]):
            anchor_pixel = anchor_pixels[xanchor, yanchor]
            target_pixel = target_pixels[target_rect.x + xanchor, target_rect.y + yanchor]
            if anchor_pixel != target_pixel:
                return False

    return True


def wait(num_ms):
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < num_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)


def find_anchor(source_pixels, sr: Rect, anchor_path):
    if not os.path.exists(anchor_path):
        raise FileNotFoundError

    anchor_surf = image.load(anchor_path).convert(32)
    anchor_pixels = PixelArray(anchor_surf)
    anchor_rect = anchor_surf.get_rect()

    anchor_hash = calc_hash(anchor_pixels, anchor_rect)

    # move through entire image, looking for a match to anchor hash
    search_rect = anchor_rect.copy()

    temp_rect = search_rect.copy()
    temp_rect.x = 1

    search_hash = 0

    for ypixel in range(sr.top, sr.bottom - anchor_rect.height):
        if ypixel == 0:
            search_hash = calc_hash(source_pixels, search_rect)
        else:
            for xxx in range(search_rect.x, search_rect.x + search_rect.width):
                search_hash ^= source_pixels[xxx, ypixel - 1]
                search_hash ^= source_pixels[xxx, search_rect.bottom]

        for xpixel in range(sr.left, sr.right - anchor_rect.width):
            search_rect.x, search_rect.y = xpixel, ypixel

            if xpixel == 0:
                search_hash = calc_hash(source_pixels, search_rect)
            else:
                # undo hashes on left side, append new ones on right
                for yyy in range(search_rect.y, search_rect.y + search_rect.height):
                    search_hash ^= source_pixels[xpixel - 1, yyy]
                    search_hash ^= source_pixels[search_rect.right, yyy]

            if search_hash == anchor_hash and is_exact_match_to_anchor(
                    anchor_pixels, anchor_rect.size, source_pixels, search_rect):
                return xpixel, ypixel

    return None


"""Given an input image of a map, slice the map into tiles and store those tiles in the specified output image"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-image', '-i', type=str)
    parser.add_argument('--dimensions', '-d', type=int, default=16)
    parser.add_argument('--out-image', '-o', type=str)
    parser.add_argument('--preview', '-p', type=bool, default=False)
    parser.add_argument('--anchor', '-a', type=str)

    args = parser.parse_args()

    input_path = args.input_image
    if input_path is None:
        parser.error("Invalid path specified")
        exit(0)

    fspath = os.fsencode(input_path)

    if not os.path.exists(fspath):
        raise FileNotFoundError

    width, height = args.dimensions, args.dimensions

    screen = None
    screen_rect = None
    preview_surf = None

    if args.preview:
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        screen_rect = screen.get_rect()
        pygame.display.set_caption("Super Mario Tileset Generator")

    source = image.load(input_path).convert(32)
    source_rect = source.get_rect()

    if args.preview:
        preview_surf = source.convert()

    picker_rect = Rect(0, 0, width, height)
    pixels = PixelArray(source)
    tiles = []

    anchor_offsets = 0, 0
    num_passed_sequential = 0
    per_tile_wait_time = 100  # ms

    if args.anchor is not None:
        result = find_anchor(pixels, source_rect, args.anchor)

        if result is None:
            print(f"Failed to find anchor {args.anchor}")
            raise RuntimeError

        anchor_offsets = result

    for y in range(anchor_offsets[1] % height, source_rect.height - anchor_offsets[1] % height, height):
        for x in range(anchor_offsets[0] % width, source_rect.width - anchor_offsets[0] % width, width):
            picker_rect.x, picker_rect.y = x, y

            if picker_rect.right > source_rect.width or picker_rect.bottom > source_rect.height \
                    or picker_rect.left < 0 or picker_rect.top < 0:
                continue

            if args.preview:
                r = source_rect.copy()
                r.x, r.y = -picker_rect.x, -picker_rect.y

                screen.fill((0, 0, 0))
                screen.blit(preview_surf, r)

                r.x, r.y = 0, 0
                r.width, r.height = picker_rect.width, picker_rect.height

                pygame.draw.rect(screen, (255, 0, 0), r, 2)
                pygame.display.flip()

                wait(per_tile_wait_time)

            hash_value = calc_hash(pixels, picker_rect)

            # identify any possible matches for this tile.
            existing = [t for t in tiles if t.hash_value == hash_value]

            if existing is not None:
                # there's at least one hash collision, but it's possible the tile is still unique
                # note: this condition separate instead of ANDed with hash value above,
                # because comparing pixel-by-pixel is much slower than just hash
                if not any(e for e in existing if is_exact_match(pixels, e.rect, picker_rect)):
                    existing = None  # none of the known tiles is exactly right

            if existing is None:
                tiles.append(_GeneratedTile(rect=picker_rect.copy(), hash_value=hash_value))
                print("Added new tile")
                wait(1000)
                num_passed_sequential = 0
                per_tile_wait_time = 100
            else:
                num_passed_sequential += 1

                if num_passed_sequential > 10:
                    num_passed_sequential = 0
                    per_tile_wait_time /= 2

    print(f"Identified {len(tiles)} unique tiles in {input_path}")
    pixels.close()

    if args.out_image is None:
        print("No output image specified; finished")
    elif len(tiles) == 0:
        print("No tiles detected")
    else:
        # compute dimensions (in terms of tiles) of a new surface to hold unique tiles
        ts_width = math.ceil(math.sqrt(len(tiles)))
        ts_height = math.ceil(float(len(tiles)) / ts_width)

        ts = Surface((ts_width * width, ts_height * height))
        ts.fill((255, 0, 255, 0))  # fill with transparent magenta

        for idx in range(len(tiles)):
            # compute position (in tiles) on new tile set
            tile_x = idx % ts_width
            tile_y = idx // ts_width

            picker_rect.x, picker_rect.y = tile_x * width, tile_y * width

            ts.blit(source, picker_rect, tiles[idx].rect)

        image.save(ts, args.out_image)
