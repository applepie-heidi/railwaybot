from typing import Optional

import pygame as pg

from app.components.board import Board, BoardGroup
from app.components.cards import DeckGroup, Card, FaceUpCardsGroup
from app.components.text import Text, TextGroup
from app.config import *
from app.scenes.dest import DestinationChooserScene
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
        self.board_group = BoardGroup(game, COLORS_DICT)
        self.text_group = TextGroup()
        self.destination_deck_group = DeckGroup()
        self.train_deck_group = DeckGroup()
        self.face_up_cards_group = FaceUpCardsGroup()
        self._add()
        self.sub_scene: Optional[Scene] = None

    def _add(self):
        board = Board(BOARD_IMAGE_PATH, PADDING, PADDING, self.railway_images)
        self.board_group.add(board)

        self._refresh_text()

        destination_deck = Card(DESTINATION_DECK_PATH, PADDING + board.rect.width + 2 * PADDING,
                                PADDING + BIG_TEXT_SIZE + len(COLORS_DICT) * (SMALL_TEXT_SIZE + 2 * PADDING),
                                CARD_VERTICAL_SIZE[0], CARD_VERTICAL_SIZE[1])
        self.destination_deck_group.add(destination_deck)

        train_deck = Card(TRAIN_DECK_PATH, PADDING + board.rect.width + 2 * PADDING,
                          PADDING + BIG_TEXT_SIZE + len(COLORS_DICT) * (SMALL_TEXT_SIZE + 2 * PADDING) + PADDING +
                          CARD_VERTICAL_SIZE[1],
                          CARD_VERTICAL_SIZE[0], CARD_VERTICAL_SIZE[1])
        self.train_deck_group.add(train_deck)

        self.game.turn_cards_face_up()
        for i, card in enumerate(self.game.face_up_cards):
            face_up_card = Card(TRAIN_IMAGES_DICT[card], SCREEN_SIZE[0] - PADDING - CARD_HORIZONTAL_SIZE[0],
                                destination_deck.rect.y - (CARD_HORIZONTAL_SIZE[1] + PADDING) +
                                i * (CARD_HORIZONTAL_SIZE[1] + PADDING),
                                CARD_HORIZONTAL_SIZE[0], CARD_HORIZONTAL_SIZE[1])
            self.face_up_cards_group.add(face_up_card)

    def _refresh_text(self):
        current_player = self.game.get_current_player()
        self.text_group.empty()

        player_text = Text(current_player.color.upper(),
                           COLORS_DICT[self.game.get_current_player().color], BIG_TEXT_SIZE,
                           PADDING + self.board_group.sprite.rect.width + 2 * PADDING, PADDING)
        self.text_group.add(player_text)

        for i, player in enumerate(self.game.players):
            player_score = Text(f"{player.color.upper()}: {player.points}", COLORS_DICT[player.color], SMALL_TEXT_SIZE,
                                PADDING + self.board_group.sprite.rect.width + 2 * PADDING,
                                PADDING + BIG_TEXT_SIZE + i * SMALL_TEXT_SIZE)
            self.text_group.add(player_score)

        for i, destination in enumerate(current_player.destination_cards):
            destination_text = Text(str(destination), (0, 0, 0), MINI_TEXT_SIZE, PADDING,
                                    PADDING + self.board_group.sprite.rect.height + PADDING + i * MINI_TEXT_SIZE)
            self.text_group.add(destination_text)

    def handle_click(self, pos):
        if self.sub_scene:
            self.sub_scene.handle_click(pos)
            if self.sub_scene.is_finished:
                self.sub_scene = None
                self.game.next_turn()
                self._refresh_text()
        else:
            self.board_group.handle_click(pos)
            self.destination_deck_group.handle_click(pos)
            if self.destination_deck_group.is_clicked:
                destinations = self.game.draw_destination_cards()
                self.sub_scene = DestinationChooserScene(self.game, destinations, MINIMUM_DESTINATION_CARDS)
                self.destination_deck_group.unclick()

    def draw(self, screen):
        if self.sub_scene:
            self.sub_scene.draw(screen)
        else:
            background = pg.Surface(SCREEN_SIZE)
            background.convert()
            background.fill(SCREEN_COLOR)
            screen.blit(background, (0, 0))
            self.board_group.draw(screen)
            self.text_group.draw(screen)
            self.destination_deck_group.draw(screen)
            self.train_deck_group.draw(screen)
            self.face_up_cards_group.draw(screen)

    @property
    def is_finished(self):
        return False
