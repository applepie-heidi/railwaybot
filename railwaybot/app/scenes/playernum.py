import pygame as pg

from app.components.buttons import PlayerNumberButtonGroup, Button
from app.config import *
from app.scenes.scene import Scene
from engine.game import Player


class NumberOfPlayersScene(Scene):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.button_group = PlayerNumberButtonGroup()
        self._add_buttons()

    def _add_buttons(self):
        button_position_x = SCREEN_SIZE[0] / 2 - (MAX_PLAYERS - 1) * (BUTTON_SIZE_X + PADDING)
        button_position_y = SCREEN_SIZE[1] / 2
        for i in range(2, MAX_PLAYERS + 1):
            button = Button(BUTTON_COLOR, BUTTON_SIZE_X, BUTTON_SIZE_X,
                            button_position_x + i * (BUTTON_SIZE_X + PADDING), button_position_y,
                            text=str(i), text_size=BIG_TEXT_SIZE, text_y=15)
            self.button_group.add(button)

    def handle_click(self, pos):
        self.button_group.handle_click(pos)
        clicked = self.button_group.get_clicked()
        if clicked:
            for i in range(int(clicked)):
                player = Player(COLORS_LIST[i], TRAINS)
                self.game.add_player(player)

    def draw(self, screen):
        background = pg.Surface(SCREEN_SIZE)
        background.convert()
        background.fill(SCREEN_COLOR)
        screen.blit(background, (0, 0))
        self.button_group.draw(screen)

    @property
    def is_finished(self):
        return bool(self.game.players)
