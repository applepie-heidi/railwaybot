import pygame as pg

from app.components.buttons import PlayerNumberButtonGroup, Button
from app.components.text import Text, TextGroup
from app.config import *
from app.scenes.scene import Scene
from engine.game import Player


class NumberOfPlayersScene(Scene):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.text_group = TextGroup()
        self.button_group = PlayerNumberButtonGroup()
        self._add()

    def _add(self):
        self.text = Text("Choose the number of players", (0, 0, 0), HUGE_TEXT_SIZE,
                         SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 - HUGE_TEXT_SIZE, center=True)
        self.text_group.add(self.text)

        button_position_x = SCREEN_SIZE[0] / 2 - (MAX_PLAYERS - 1) * (BUTTON_SIZE_X + PADDING)
        button_position_y = SCREEN_SIZE[1] / 2
        for i in range(2, MAX_PLAYERS + 1):
            button = Button(BUTTON_COLOR, BUTTON_SIZE_X, BUTTON_SIZE_X,
                            button_position_x + i * (BUTTON_SIZE_X + PADDING), button_position_y,
                            text=str(i), text_size=HUGE_TEXT_SIZE, text_y=15)
            self.button_group.add(button)

    def handle_click(self, pos):
        self.button_group.handle_click(pos)
        clicked = self.button_group.get_clicked_text()
        if clicked:
            self.game.add_players(COLORS_LIST[:int(clicked)], TRAINS)

    def draw(self, screen):
        background = pg.Surface(SCREEN_SIZE)
        background.convert()
        background.fill(SCREEN_COLOR)
        screen.blit(background, (0, 0))
        self.text_group.draw(screen)
        self.button_group.draw(screen)

    @property
    def is_finished(self):
        return bool(self.game.players)
