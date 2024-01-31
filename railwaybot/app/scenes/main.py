from typing import Optional

import pygame as pg

from app.components.board import Board, BoardGroup
from app.config import *
from app.scenes.scene import Scene


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


class MainScene(Scene):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.railway_images = load_railway_images(RAILWAY_IMAGES_DIRECTORY)
        self.board_group = BoardGroup()
        self._add()
        self.sub_scene: Optional[Scene] = None

    def _add(self):
        board = Board(BOARD_IMAGE_PATH, BOARD_POSITION[0], BOARD_POSITION[1], self.railway_images)
        self.board_group.add(board)

    def handle_click(self, pos):
        self.board_group.handle_click(pos)

    def draw(self, screen):
        if self.sub_scene is not None:
            self.sub_scene.draw(screen)
        else:
            background = pg.Surface(SCREEN_SIZE)
            background.convert()
            background.fill(SCREEN_COLOR)
            screen.blit(background, (0, 0))
            self.board_group.draw(screen)


    @property
    def is_finished(self):
        return False
