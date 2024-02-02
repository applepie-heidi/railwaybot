from typing import Optional

import pygame as pg

from app.components.board import BoardGroup
from app.components.cards import DeckGroup, Card, CardsGroup
from app.components.text import Text, TextGroup
from app.config import *
from app.scenes.dest import DestinationChooserScene
from app.scenes.scene import Scene
from engine.game import Game


class MainScene(Scene):
    def __init__(self, game: Game, railway_images):
        super().__init__()
        self.game = game
        self.railway_images = railway_images
        self.board_group = BoardGroup(game, COLORS_DICT, BOARD_IMAGE_PATH, PADDING, PADDING)
        self.text_group = TextGroup()
        self.destination_deck_group = DeckGroup()
        self.train_deck_group = DeckGroup()
        self.face_up_cards_group = CardsGroup()
        self.mini_cards_group = CardsGroup()
        self.route_claiming_cards_group = CardsGroup()
        self.route_claiming_cards = []
        self._add()
        self.sub_scene: Optional[Scene] = None
        self.draws_left = CARDS_DRAW
        self.final_round = False
        self.final_turns_left = len(self.game.players)
        self._finished = False

    def _add(self):
        # board = Board(BOARD_IMAGE_PATH, PADDING, PADDING)
        # self.board_group.add(board)
        # board = self.board_group.board

        self._refresh_text()

        destination_deck = Card(DESTINATION_DECK_PATH, PADDING + self.board_group.sprite.rect.width + 2 * PADDING,
                                PADDING + BIG_TEXT_SIZE + len(COLORS_DICT) * (SMALL_TEXT_SIZE + 2 * PADDING),
                                CARD_VERTICAL_SIZE[0], CARD_VERTICAL_SIZE[1])
        self.destination_deck_group.add(destination_deck)

        train_deck = Card(TRAIN_DECK_PATH, PADDING + self.board_group.sprite.rect.width + 2 * PADDING,
                          PADDING + BIG_TEXT_SIZE + len(COLORS_DICT) * (SMALL_TEXT_SIZE + 2 * PADDING) + PADDING +
                          CARD_VERTICAL_SIZE[1],
                          CARD_VERTICAL_SIZE[0], CARD_VERTICAL_SIZE[1])
        self.train_deck_group.add(train_deck)

        self.game.turn_cards_face_up()
        self._refresh_face_up_cards()

        for i, color in enumerate(TRAIN_COLORS_LIST):
            mini_card = Card(TRAIN_IMAGES_DICT[color],
                             PADDING + DESTINATIONS_PADDING + i * (MINI_CARD_SIZE[0] + PADDING),
                             SCREEN_SIZE[1] - PADDING - MINI_CARD_SIZE[1] - MINI_TEXT_SIZE - PADDING,
                             MINI_CARD_SIZE[0], MINI_CARD_SIZE[1], color=color)
            self.mini_cards_group.add(mini_card)

    def _refresh_text(self):
        current_player = self.game.get_current_player()
        self.text_group.empty()

        player_text = Text(current_player.color.upper(),
                           COLORS_DICT[self.game.get_current_player().color], BIG_TEXT_SIZE,
                           PADDING + self.board_group.sprite.rect.width + 2 * PADDING, PADDING)
        self.text_group.add(player_text)

        for i, player in enumerate(self.game.players):
            player_score = Text(f"{player.color.upper()}: {player.points} ({player.trains} trains)",
                                COLORS_DICT[player.color], SMALL_TEXT_SIZE,
                                PADDING + self.board_group.sprite.rect.width + 2 * PADDING,
                                PADDING + BIG_TEXT_SIZE + i * SMALL_TEXT_SIZE)
            self.text_group.add(player_score)

        for i, destination in enumerate(current_player.destination_cards):
            destination_text = Text(str(destination), (0, 0, 0), MINI_TEXT_SIZE, PADDING,
                                    PADDING + self.board_group.sprite.rect.height + PADDING + i * MINI_TEXT_SIZE)
            self.text_group.add(destination_text)

        cards_dict = {i: 0 for i in TRAIN_COLORS_LIST}
        for card in current_player.cards:
            cards_dict[card] += 1
        for i, card in enumerate(cards_dict):
            if cards_dict[card] == 0:
                color = (128, 128, 128)
            else:
                color = (0, 0, 0)
            card_text = Text(str(cards_dict[card]), color, MINI_TEXT_SIZE,
                             PADDING + DESTINATIONS_PADDING + i * (MINI_CARD_SIZE[0] + PADDING) + MINI_CARD_SIZE[0] / 2,
                             SCREEN_SIZE[1] - PADDING - MINI_TEXT_SIZE)
            self.text_group.add(card_text)

    def _refresh_face_up_cards(self):
        self.face_up_cards_group.empty()
        for i, card in enumerate(self.game.face_up_cards):
            face_up_card = Card(TRAIN_IMAGES_DICT[card], SCREEN_SIZE[0] - PADDING - CARD_HORIZONTAL_SIZE[0],
                                self.destination_deck_group.sprite.rect.y - (CARD_HORIZONTAL_SIZE[1] + PADDING) +
                                i * (CARD_HORIZONTAL_SIZE[1] + PADDING),
                                CARD_HORIZONTAL_SIZE[0], CARD_HORIZONTAL_SIZE[1], color=card)
            self.face_up_cards_group.add(face_up_card)

    def _refresh_route_claiming_cards(self):
        self.route_claiming_cards_group.empty()
        for i, card in enumerate(self.route_claiming_cards):
            route_claiming_card = Card(TRAIN_IMAGES_DICT[card],
                                       PADDING + DESTINATIONS_PADDING + 5 * PADDING + CARD_HORIZONTAL_SIZE[0] + (
                                               i % 3) * (
                                               CARD_HORIZONTAL_SIZE[0] + PADDING),
                                       PADDING + self.board_group.sprite.rect.height + PADDING + (
                                               i // 3) * (CARD_HORIZONTAL_SIZE[1] + PADDING),
                                       CARD_HORIZONTAL_SIZE[0], CARD_HORIZONTAL_SIZE[1], color=card)
            self.route_claiming_cards_group.add(route_claiming_card)

    def handle_click(self, pos):
        if self.sub_scene:
            self.sub_scene.handle_click(pos)
            if self.sub_scene.is_finished:
                self.sub_scene = None
                self.game.next_turn()
                self._refresh_text()
                if self.final_round:
                    self.do_final_round()
        else:
            if self.draws_left == CARDS_DRAW:
                if not self.route_claiming_cards_group.sprites():
                    self.destination_deck_group.handle_click(pos)
                else:
                    colors_count = {}
                    for color in self.route_claiming_cards:
                        colors_count[color] = colors_count.get(color, 0) + 1
                    railway_images = self._calc_relevant_railways(colors_count)
                    self.board_group.set_railway_images(railway_images)
                    self.board_group.handle_click(pos)
                    if self.board_group.clicked_railway:
                        railways = self.game.board.get_railways(self.board_group.clicked_railway[0],
                                                                self.board_group.clicked_railway[1])
                        if railways:
                            railway = railways[0]
                            if len(railways) == 2:
                                railway2 = railways[1]
                                if len(self.game.players) <= 3:
                                    if railway.color == self.board_group.clicked_railway[2].strip("x"):
                                        self.game.claim_railway(railway, self.route_claiming_cards,
                                                                parallel_railway=railway2)
                                        self.route_claiming_cards = []
                                        self._refresh_route_claiming_cards()
                                    else:
                                        self.game.claim_railway(railway2, self.route_claiming_cards,
                                                                parallel_railway=railway)
                                        self.route_claiming_cards = []
                                        self._refresh_route_claiming_cards()
                                else:
                                    if railway.color == self.board_group.clicked_railway[2].strip("x"):
                                        self.game.claim_railway(railway, self.route_claiming_cards)
                                        self.route_claiming_cards = []
                                        self._refresh_route_claiming_cards()
                                    else:
                                        self.game.claim_railway(railway2, self.route_claiming_cards)
                                        self.route_claiming_cards = []
                                        self._refresh_route_claiming_cards()
                            else:
                                self.game.claim_railway(railway, self.route_claiming_cards)
                                self.route_claiming_cards = []
                                self._refresh_route_claiming_cards()

                        if self.final_round:
                            self.do_final_round()
                        if self.game.get_current_player().trains <= 2:
                            self.final_round = True
                        self.board_group.remove_clicked_railway()
                        self.game.next_turn()
                        self._refresh_text()

                self.route_claiming_cards_group.handle_click(pos)
                self.mini_cards_group.handle_click(pos)
            if ((self.draws_left == CARDS_DRAW and len(self.game.cards) >= CARDS_DRAW) or (
                    self.draws_left == CARDS_DRAW - 1 and len(self.game.cards) >= CARDS_DRAW - 1)) and (
                    not self.route_claiming_cards_group.sprites()):
                self.train_deck_group.handle_click(pos)
                self.face_up_cards_group.handle_click(pos)

            if self.destination_deck_group.is_clicked:
                destinations = self.game.draw_destination_cards()
                self.sub_scene = DestinationChooserScene(self.game, destinations, MINIMUM_DESTINATION_CARDS)
                self.destination_deck_group.unclick()
            elif self.train_deck_group.is_clicked:
                self.draw_deck_train_card()
                self.train_deck_group.unclick()
                if self.draws_left == 0:
                    self.game.next_turn()
                    self._refresh_text()
                    self.draws_left = CARDS_DRAW
                    if self.final_round:
                        self.do_final_round()
                self._refresh_text()
            elif self.face_up_cards_group.get_clicked_card():
                self.draw_face_up_train_card(self.face_up_cards_group.clicked_card.color)
                self.face_up_cards_group.remove_clicked_card()
                if self.draws_left == 0:
                    self.game.next_turn()
                    self._refresh_text()
                    self.draws_left = CARDS_DRAW
                    if self.final_round:
                        self.do_final_round()
                self._refresh_face_up_cards()
                self._refresh_text()
            elif self.mini_cards_group.get_clicked_card():
                if len(self.route_claiming_cards_group.sprites()) < ROUTE_MAX_LENGTH:
                    self.put_route_claiming_card()
                self.mini_cards_group.remove_clicked_card()
                self._refresh_text()
            elif self.route_claiming_cards_group.get_clicked_card():
                self.remove_route_claiming_card()
                self.route_claiming_cards_group.remove_clicked_card()
                self._refresh_text()

    def _calc_relevant_railways(self, colors_count):
        railway_images = {}
        for railway_image in self.railway_images:
            length = 0
            if len(colors_count) <= 2:
                if railway_image[2].strip("x") == "grey":
                    length = sum(colors_count.values())
                else:
                    length = colors_count.get(railway_image[2].strip("x"), 0) + colors_count.get(ANY_COLOR,
                                                                                                 0)
            railways = self.game.board.get_railways(railway_image[0], railway_image[1])
            for railway in railways:
                if length == railway.length and self.game.get_current_player().trains >= railway.length:
                    if not railway.claimed and railway.color == railway_image[2].strip("x"):
                        railway_images[railway_image] = self.railway_images[railway_image]
        return railway_images

    def put_route_claiming_card(self):
        color = self.mini_cards_group.get_clicked_card().color
        if color in self.game.get_current_player().cards:
            self.route_claiming_cards.append(color)
            self.game.get_current_player().remove_card(color)
            self._refresh_route_claiming_cards()

    def remove_route_claiming_card(self):
        color = self.route_claiming_cards_group.get_clicked_card().color
        self.route_claiming_cards.remove(color)
        self.game.get_current_player().add_card(color)
        self._refresh_route_claiming_cards()

    def draw_deck_train_card(self):
        card = self.game.draw_card()
        self.game.get_current_player().add_card(card)
        self.draws_left -= 1

    def draw_face_up_train_card(self, color):
        if self.draws_left == CARDS_DRAW or (self.draws_left == CARDS_DRAW - 1 and color != ANY_COLOR):
            card = self.game.draw_card(color)
            self.game.get_current_player().add_card(card)
            if color == ANY_COLOR:
                self.draws_left -= 2
            else:
                self.draws_left -= 1

    def do_final_round(self):
        self.final_turns_left -= 1
        if self.final_turns_left == 0:
            self._finished = True

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
            self.mini_cards_group.draw(screen)
            self.route_claiming_cards_group.draw(screen)

    @property
    def is_finished(self):
        return self._finished
