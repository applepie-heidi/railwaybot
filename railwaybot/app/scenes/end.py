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
        self.game.final_scoring()
        self.railway_images = railway_images
        self.text_group = TextGroup()
        self.board_group = BoardGroup.from_finished_game(game, self.railway_images, COLORS_DICT, BOARD_IMAGE_PATH,
                                                         SCREEN_SIZE[0] / 2 - BOARD_SIZE[0] / 2,
                                                         PADDING)
        self._add()

    def _add(self):
        winner = max(self.game.players, key=lambda x: x.points)
        winner_text = Text(f"The winner is {winner.color.upper()}", COLORS_DICT[winner.color],
                           HUGE_TEXT_SIZE, SCREEN_SIZE[0] / 2, PADDING + BOARD_SIZE[1] + PADDING, center=True)
        self.text_group.add(winner_text)

        for i, player in enumerate(self.game.players):
            text = Text(f"Player {player.color.upper()} has {player.points} points", COLORS_DICT[player.color],
                        SMALL_TEXT_SIZE, SCREEN_SIZE[0] / 2,
                        PADDING + BOARD_SIZE[1] + PADDING + HUGE_TEXT_SIZE + i * SMALL_TEXT_SIZE,
                        center=True)
            self.text_group.add(text)

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
