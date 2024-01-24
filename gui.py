import os

import pygame as pg
from pygame import PixelArray

BOARD_OFFSET = (10, 10)


def load_railway_images(image_directory):
    railway_images = {}
    # traverse given directory and load all images
    for filename in os.listdir(image_directory):
        if filename.endswith(".png"):
            image = load_image(os.path.join(image_directory, filename))
            railway_images[filename[:-4]] = image


def load_image(path, colorkey=None):
    image = pg.image.load(path)
    image = image.convert_alpha()
    if colorkey:
        image.set_colorkey(colorkey)
    return image


def main():
    pg.init()
    screen = pg.display.set_mode((1400, 900), pg.SCALED)
    screen.fill((220, 216, 215))

    board = load_image("data/images/board.png")
    screen.blit(board, BOARD_OFFSET)

    mask_image = load_image("data/images/mask_test.png")
    pixels = PixelArray(mask_image)
    pixels.replace((255, 2, 0), (255, 255, 0))
    del pixels
    mask = pg.mask.from_surface(mask_image)

    clock = pg.time.Clock()
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if is_click_inside_mask(event.pos, mask):
                    draw_masked_area(screen, board, mask_image)

        pg.display.flip()
        clock.tick(60)


def is_click_inside_mask(click_pos, mask):
    relative_pos = (click_pos[0] - BOARD_OFFSET[0], click_pos[1] - BOARD_OFFSET[1])
    return mask.get_at(relative_pos)


def draw_masked_area(screen, board, mask_image):
    result_image = pg.Surface(board.get_size())
    result_image = result_image.convert_alpha()
    result_image.fill((255, 255, 255))
    result_image.blit(mask_image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    screen.blit(result_image, BOARD_OFFSET)


if __name__ == '__main__':
    main()
