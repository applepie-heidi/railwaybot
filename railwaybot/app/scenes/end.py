import pygame as pg

from app.components.board import Board, BoardGroup
from app.components.text import TextGroup, Text
from app.config import *
from app.scenes.scene import Scene
from engine.game import Game


class GameEndScene(Scene):
    def __init__(self, game: Game, railway_images):
        super().__init__()
        self.game = game
        self.railway_images = railway_images
        self.text_group = TextGroup()
        self.board_group = BoardGroup.from_finished_game(game, self.railway_images, COLORS_DICT, BOARD_IMAGE_PATH, 20, 20)
        self._add()

    def _add(self):
        self.text = Text("Game Over", (0, 0, 0), HUGE_TEXT_SIZE,
                         SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 - HUGE_TEXT_SIZE, center=True)
        self.text_group.add(self.text)

    def draw(self, screen):
        background = pg.Surface(SCREEN_SIZE)
        background.convert()
        background.fill(SCREEN_COLOR)
        screen.blit(background, (0, 0))
        self.text_group.draw(screen)
        self.board_group.draw(screen)

    @property
    def is_finished(self):
        return True
