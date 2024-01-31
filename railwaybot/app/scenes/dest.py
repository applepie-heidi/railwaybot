import pygame as pg

from app.components.buttons import Button, ToggleButtonGroup, ToggleButton, OkButtonGroup
from app.components.text import TextGroup, Text
from app.config import *
from app.scenes.scene import Scene


class DestinationChooserScene(Scene):
    def __init__(self, game, destinations, minimum_selected, current_player=None):
        super().__init__()
        self.game = game
        self.destinations = destinations
        self.minimum_selected = minimum_selected
        if not current_player:
            self.current_player = self.game.get_current_player()
        else:
            self.current_player = current_player
        self._finished = False
        self.text_group = TextGroup()
        self.dest_group = ToggleButtonGroup()
        self.ok_button_group = OkButtonGroup()
        self._add()

    def _add(self):
        text = Text(f"Choose a minimum of {self.minimum_selected} cards", (0, 0, 0), BIG_TEXT_SIZE,
                    SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 - BIG_TEXT_SIZE, center=True)
        player_text = Text(f"Player {self.current_player.color.upper()}", COLORS_DICT[self.current_player.color], BIG_TEXT_SIZE,
                           SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 - 2 * BIG_TEXT_SIZE, center=True)
        self.text_group.add(text)
        self.text_group.add(player_text)

        self.ok_button = Button(BUTTON_COLOR, BUTTON_SIZE_X, BUTTON_SIZE_X,
                                SCREEN_SIZE[0] / 2 + DESTINATION_SIZE[0],
                                SCREEN_SIZE[1] / 2 + DESTINATION_SIZE[1] + PADDING,
                                text="Choose", text_size=SMALL_TEXT_SIZE, text_y=40)
        self.ok_button_group.add(self.ok_button)

        button_position_x = SCREEN_SIZE[0] / 2 - 1.5 * (DESTINATION_SIZE[0] + PADDING)
        button_position_y = SCREEN_SIZE[1] / 2
        for i, destination in enumerate(self.destinations):
            button = ToggleButton(DESTINATION_COLOR, DESTINATION_SIZE[0], DESTINATION_SIZE[1],
                                  button_position_x + i * (DESTINATION_SIZE[0] + PADDING), button_position_y,
                                  text=str(destination), text_size=SMALL_TEXT_SIZE, text_y=40)
            self.dest_group.add(button)

    def handle_click(self, pos):
        self.dest_group.handle_click(pos)
        if len(self.dest_group.get_selected()) >= self.minimum_selected:
            self.ok_button_group.handle_click(pos)
            if self.ok_button_group.is_clicked:
                self._finished = True
                destinations = self.destinations.copy()
                for destination in self.destinations:
                    for selected in self.dest_group.get_selected():
                        if str(destination) == selected:
                            self.current_player.add_destination(destination)
                            destinations.remove(destination)
                self.game.discard_destination_cards(destinations)

    def draw(self, screen):
        background = pg.Surface(SCREEN_SIZE)
        background.convert()
        background.fill(SCREEN_COLOR)
        screen.blit(background, (0, 0))
        self.text_group.draw(screen)
        self.dest_group.draw(screen)
        if len(self.dest_group.get_selected()) >= self.minimum_selected:
            self.ok_button_group.draw(screen)

    @property
    def is_finished(self):
        return self._finished
