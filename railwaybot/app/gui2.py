from __future__ import annotations

import pygame as pg

from app.config import *
from app.scenes.end import GameEndScene
from app.scenes.main import MainScene
from app.scenes.setup import SetupScene
from engine.game import Game


def load_image(path, color_key=None, scale=1.0):
    image = pg.image.load(path)
    image = image.convert_alpha()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if color_key:
        image.set_colorkey(color_key)
    return image


def load_railway_images(image_directory):
    railway_images = {}
    for filename in os.listdir(image_directory):
        if filename.endswith(".png"):
            image = load_image(os.path.join(image_directory, filename))
            image_name_list = filename[:-4].replace("_", " ").split("-")
            image_name = (image_name_list[0], image_name_list[1], image_name_list[2])
            railway_images[image_name] = image
    return railway_images


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
    pg.display.set_caption("Ticket to Ride")

    game = Game(BOARD_PATH, DESTINATION_CARDS_PATH, TRAIN_CARDS_PATH, SCORING_PATH)

    clock = pg.time.Clock()

    done = False

    current_scene = SetupScene(game)
    railway_images = load_railway_images(RAILWAY_IMAGES_DIRECTORY)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if current_scene:
                    current_scene.handle_click(event.pos)

            if current_scene and current_scene.is_finished:
                if isinstance(current_scene, SetupScene):
                    current_scene = MainScene(game, railway_images)
                elif isinstance(current_scene, MainScene):
                    current_scene = GameEndScene(game, railway_images)

        if done:
            break

        current_scene and current_scene.draw(screen)
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
