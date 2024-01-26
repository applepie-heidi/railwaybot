from __future__ import annotations
from typing import Tuple
import json
import os
import random

import pygame as pg
from pygame import PixelArray

from engine.game import Game, Player, ANY_COLOR


def parse_player_json():
    with open(PLAYER_PATH, "r") as f:
        data = json.load(f)
        colors = {}
        for color in data["colors"]:
            colors[color["name"]] = (color["r"], color["g"], color["b"])
        return colors, data["trains_per_player"]


def parse_train_images():
    train_images = {}
    # traverse given directory and load all images
    for filename in os.listdir(TRAIN_IMAGES_DIRECTORY):
        if filename.endswith(".png"):
            train_images[filename[:-4]] = TRAIN_IMAGES_DIRECTORY + "/" + filename
    return train_images


def get_shuffled_colors(colors):
    shuffled_colors = []
    for color in colors:
        shuffled_colors.append(color)
    random.shuffle(shuffled_colors)
    return shuffled_colors


BOARD_PATH = "data/jsons/board.json"
DESTINATION_CARDS_PATH = "data/jsons/destination_cards.json"
TRAIN_CARDS_PATH = "data/jsons/train_cards.json"
SCORING_PATH = "data/jsons/scoring.json"
PLAYER_PATH = "data/jsons/player.json"
RAILWAY_IMAGES_DIRECTORY = "data/images/railways"
TRAIN_IMAGES_DIRECTORY = "data/images/trains"
BOARD_IMAGE_PATH = "data/images/board.png"
DESTINATION_DECK_PATH = "data/images/destination_back.png"
TRAIN_DECK_PATH = "data/images/train_back.png"
TRAIN_EMPTY_PATH = "data/images/train_empty.png"
COLORS_DICT, TRAINS = parse_player_json()
COLORS_LIST = get_shuffled_colors(COLORS_DICT)
TRAIN_IMAGES_DICT = parse_train_images()
TRAIN_COLORS_LIST = get_shuffled_colors(TRAIN_IMAGES_DICT)
SCREEN_COLOR = (220, 216, 215)
BUTTON_COLOR = (141, 54, 34)
DESTINATION_COLOR = (123, 147, 147)
BUTTON_SIZE_X = 100
BIG_TEXT_SIZE = 100
SMALL_TEXT_SIZE = 30
MINI_TEXT_SIZE = 20
BOARD_POSITION = (10, 10)
DESTINATION_SIZE = (350, 100)
ROUTE_MAX_LENGTH = 6


class Button(pg.sprite.Sprite):
    def __init__(self, color, width, height, x, y, text=None, text_size=0, text_y=0):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pg.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.text = text
        self.text_size = text_size
        self.text_y = text_y
        if self.text:
            self._blit_text()
        self.rect.x = x
        self.rect.y = y

    def update(self, delete=False, color=None):
        if delete:
            self.image.fill(SCREEN_COLOR)
        else:
            if color:
                self.color = color
                self.image.fill(color)
            if self.text:
                self._blit_text()

    def add_text(self, text, text_size, text_y):
        self.image.fill(self.color)
        self.text = text
        self.text_size = text_size
        self.text_y = text_y
        self._blit_text()

    def _blit_text(self):
        font = pg.font.Font(None, self.text_size)
        text_image = font.render(self.text, True, (0, 0, 0))
        text_pos = text_image.get_rect(centerx=self.image.get_width() / 2, y=self.text_y)
        self.image.blit(text_image, text_pos)


class Text(pg.sprite.Sprite):
    def __init__(self, text, color, size, x, y, center=False):
        pg.sprite.Sprite.__init__(self)
        font = pg.font.Font(None, size)
        self.text = text
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()
        if center:
            self.rect.x = x - self.image.get_width() / 2
        else:
            self.rect.x = x
        self.rect.y = y

    def update(self, delete=False):
        if delete:
            self.image.fill(SCREEN_COLOR)


class Deck(pg.sprite.Sprite):
    def __init__(self, image_path):
        pg.sprite.Sprite.__init__(self)
        self.image_path = image_path
        self.image = load_image(image_path, scale=0.5)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, delete=False, draw=False):
        if delete:
            self.image.fill(SCREEN_COLOR)
        if draw:
            self.image = load_image(self.image_path, scale=0.5)
            self.image = self.image.convert_alpha()


class FaceUpCard(pg.sprite.Sprite):
    def __init__(self, image_path):
        pg.sprite.Sprite.__init__(self)
        self.color = None
        self.image = load_image(image_path, scale=0.5)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, delete=False, color=None, image_path=None):
        if delete:
            self.color = None
            self.image.fill(SCREEN_COLOR)
        else:
            if image_path:
                self.color = color
                self.image = load_image(image_path, scale=0.5)
                self.image = self.image.convert_alpha()


class MiniCard(pg.sprite.Sprite):
    def __init__(self, color, image_path):
        pg.sprite.Sprite.__init__(self)
        self.image_path = image_path
        self.color = color
        self.image = load_image(image_path, scale=0.3)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, delete=False, draw=False):
        if delete:
            self.image.fill(SCREEN_COLOR)
        if draw:
            self.image = load_image(self.image_path, scale=0.3)
            self.image = self.image.convert_alpha()


def load_railway_images(image_directory):
    railway_images = {}
    # traverse given directory and load all images
    for filename in os.listdir(image_directory):
        if filename.endswith(".png"):
            image = load_image(os.path.join(image_directory, filename))
            image_name_list = filename[:-4].replace("_", " ").split("-")
            image_name = (image_name_list[0], image_name_list[1], image_name_list[2])
            railway_images[image_name] = image
    return railway_images


def load_image(path, color_key=None, scale=1.0):
    image = pg.image.load(path)
    image = image.convert_alpha()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if color_key:
        image.set_colorkey(color_key)
    return image


def replace_color(image, old_color, new_color):
    pixels = PixelArray(image)
    pixels.replace(old_color, new_color)
    del pixels


def create_players(game, players_num):
    for i in range(players_num):
        player = Player(COLORS_LIST[i], TRAINS)
        game.add_player(player)


def create_choose_players_num_buttons(button_position):
    button_position_x = button_position[0] - 4 * (BUTTON_SIZE_X + 10)
    button_position_y = button_position[1]
    button_sprites = pg.sprite.Group()
    for i in range(2, len(COLORS_DICT) + 1):
        button = Button(BUTTON_COLOR, BUTTON_SIZE_X, BUTTON_SIZE_X, button_position_x + i * (BUTTON_SIZE_X + 10),
                        button_position_y, text=str(i), text_size=BIG_TEXT_SIZE, text_y=15)
        button_sprites.add(button)
    return button_sprites


def create_choose_destination_cards_buttons(button_position):
    button_position_x = button_position[0] - 1.5 * (DESTINATION_SIZE[0] + 10)
    button_position_y = button_position[1]
    button_sprites = pg.sprite.Group()

    for i in range(3):
        button = Button(DESTINATION_COLOR, DESTINATION_SIZE[0], DESTINATION_SIZE[1],
                        button_position_x + i * (DESTINATION_SIZE[0] + 10), button_position_y)
        button_sprites.add(button)

    return button_sprites


def create_decks_and_face_ups(screen_x, board_x):
    train_cards_action_sprites = pg.sprite.Group()
    destination_deck_sprite = pg.sprite.GroupSingle()
    train_deck_sprite = pg.sprite.GroupSingle()

    destination_deck = Deck(DESTINATION_DECK_PATH)
    destination_deck_sprite.add(destination_deck)

    for i in range(5):
        face_up_card = FaceUpCard(TRAIN_EMPTY_PATH)
        train_cards_action_sprites.add(face_up_card)

    destination_deck.rect.x = BOARD_POSITION[0] + board_x + 20
    destination_deck.rect.y = BOARD_POSITION[0] + BIG_TEXT_SIZE + 5 * (SMALL_TEXT_SIZE + 20)

    for card in train_cards_action_sprites.sprites():
        card.rect.x = screen_x - card.rect.width - 10
        card.rect.y = destination_deck.rect.y - card.rect.height + (
                train_cards_action_sprites.sprites().index(card) * (card.rect.height + 10))

    train_deck = Deck(TRAIN_DECK_PATH)
    train_deck_sprite.add(train_deck)
    train_deck.rect.x = destination_deck.rect.x
    train_deck.rect.y = destination_deck.rect.y + destination_deck.rect.height + 10

    return destination_deck_sprite, train_deck_sprite, train_cards_action_sprites


def create_mini_cards(screen_y):
    mini_card_sprites = pg.sprite.Group()
    for color in TRAIN_COLORS_LIST:
        mini_card = MiniCard(color, TRAIN_IMAGES_DICT[color])
        mini_card.rect.x = BOARD_POSITION[0] + 250 + (TRAIN_COLORS_LIST.index(color) * (mini_card.rect.width + 10))
        mini_card.rect.y = screen_y - mini_card.rect.height - BOARD_POSITION[1] - MINI_TEXT_SIZE - 10
        mini_card_sprites.add(mini_card)
    return mini_card_sprites


def create_route_claiming_cards(screen_y, board_y):
    route_claiming_cards_sprites = pg.sprite.Group()
    for i in range(ROUTE_MAX_LENGTH):
        card = FaceUpCard(TRAIN_EMPTY_PATH)
        card.rect.x = BOARD_POSITION[0] + 300 + card.rect.width + ((i % 3) * (card.rect.width + 10))
        card.rect.y = board_y + BOARD_POSITION[1] + 10 + (i // 3) * (card.rect.height + 10)
        route_claiming_cards_sprites.add(card)
    return route_claiming_cards_sprites


def main():
    pg.init()
    screen = pg.display.set_mode((1300, 1000), pg.SCALED)
    pg.display.set_caption("Ticket to Ride")

    screen.fill(SCREEN_COLOR)

    game = Game(BOARD_PATH, DESTINATION_CARDS_PATH, TRAIN_CARDS_PATH, SCORING_PATH)

    choose_button_text = Text("Choose the number of players", (0, 0, 0), BIG_TEXT_SIZE, screen.get_width() / 2,
                              screen.get_height() / 2 - BIG_TEXT_SIZE, center=True)
    button_sprites = create_choose_players_num_buttons((screen.get_width() / 2, screen.get_height() / 2))
    button_sprites.add(choose_button_text)

    current_player_text_sprite = pg.sprite.GroupSingle()

    minimum_destination_cards = 2
    destination_button_sprites = create_choose_destination_cards_buttons(
        (screen.get_width() / 2, screen.get_height() / 2))
    clicked_destination_button_sprites = pg.sprite.Group()
    choose_destination_cards_text = Text(f"Choose a minimum of {minimum_destination_cards} cards", (0, 0, 0),
                                         BIG_TEXT_SIZE,
                                         screen.get_width() / 2, screen.get_height() / 2 - BIG_TEXT_SIZE, center=True)
    destination_button_text_sprite = pg.sprite.GroupSingle()
    destination_button_text_sprite.add(choose_destination_cards_text)
    chosen_destination_button = Button(BUTTON_COLOR, BUTTON_SIZE_X, BUTTON_SIZE_X,
                                       screen.get_width() / 2 + DESTINATION_SIZE[0],
                                       screen.get_height() / 2 + DESTINATION_SIZE[1] + 10, text="Choose",
                                       text_size=SMALL_TEXT_SIZE, text_y=40)
    chosen_destination_button_sprite = pg.sprite.GroupSingle()
    chosen_destination_button_sprite.add(chosen_destination_button)
    chosen_destination_button_sprite.update(delete=True)
    all_destination_sprites = pg.sprite.Group()
    all_destination_sprites.add(destination_button_sprites,
                                destination_button_text_sprite, chosen_destination_button_sprite)
    destination_cards = game.draw_destination_cards()

    railway_images = load_railway_images(RAILWAY_IMAGES_DIRECTORY)
    railway_masks = {}
    for image_name in railway_images:
        choice = random.choice(COLORS_LIST)
        replace_color(railway_images[image_name], (0, 0, 0), COLORS_DICT[choice])
        railway_masks[image_name] = pg.mask.from_surface(railway_images[image_name])

    board = load_image(BOARD_IMAGE_PATH)
    board = board.convert_alpha()
    board_cover = pg.Surface(board.get_size())
    board_cover = board_cover.convert_alpha()
    board_cover.fill(SCREEN_COLOR)

    scores_text_sprites = pg.sprite.Group()

    chosen_destinations_text_sprites = pg.sprite.Group()

    destination_deck_sprite, train_deck_sprite, train_cards_action_sprites = create_decks_and_face_ups(
        screen.get_width(), board.get_width())

    mini_cards_sprites = create_mini_cards(screen.get_height())
    mini_numbers_sprites = pg.sprite.Group()

    route_claiming_cards_sprites = create_route_claiming_cards(screen.get_height(), board.get_height())
    clicked_route_claiming_cards_sprites = pg.sprite.Group()

    all_game_turn_sprites = pg.sprite.Group()
    all_game_turn_sprites.add(scores_text_sprites, chosen_destinations_text_sprites, destination_deck_sprite,
                              train_deck_sprite, train_cards_action_sprites, mini_cards_sprites, mini_numbers_sprites)

    clock = pg.time.Clock()
    game_setup = True
    choosing_destinations = False
    draws_left = 2
    turn_action = False
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if game.started:
                    if choosing_destinations:
                        destinations_chosen = False
                        destination = destination_click(event.pos, destination_button_sprites)
                        if len(clicked_destination_button_sprites.sprites()) >= minimum_destination_cards:
                            destinations_chosen = choose_destination_click(event.pos, chosen_destination_button)
                        if destinations_chosen:
                            all_destination_sprites.update(delete=True)
                            all_destination_sprites.draw(screen)

                            current_player = game.get_current_player()
                            card1 = destination_cards[0]
                            card2 = destination_cards[1]
                            card3 = destination_cards[2]
                            for button in clicked_destination_button_sprites:
                                if button.text == str(card1):
                                    current_player.add_destination_card(card1)
                                    destination_cards.remove(card1)
                                elif button.text == str(card2):
                                    current_player.add_destination_card(card2)
                                    destination_cards.remove(card2)
                                elif button.text == str(card3):
                                    current_player.add_destination_card(card3)
                                    destination_cards.remove(card3)
                            game.discard_destination_cards(destination_cards)
                            destination_cards = []
                            clicked_destination_button_sprites.empty()

                            game.next_turn()
                            switch_player_text(screen, game, board, current_player_text_sprite)
                            if game.turn == 0 and game_setup:
                                minimum_destination_cards = 1
                                game_setup = False
                                game.turn_cards_face_up()
                                turn_face_up_cards(game, train_cards_action_sprites, TRAIN_IMAGES_DICT)
                            elif game.turn != 0 and game_setup:
                                destination_cards = game.draw_destination_cards()
                                destination_button_sprites.update(color=DESTINATION_COLOR)
                                choose_destination_cards_text = Text(
                                    f"Choose a minimum of {minimum_destination_cards} cards", (0, 0, 0),
                                    BIG_TEXT_SIZE, screen.get_width() / 2, screen.get_height() / 2 - BIG_TEXT_SIZE,
                                    center=True)
                                destination_button_text_sprite.add(choose_destination_cards_text)
                            if not game_setup:
                                choosing_destinations = False
                                turn_action = True
                                destination_deck_sprite.update(draw=True)
                                turn_face_up_cards(game, train_cards_action_sprites, TRAIN_IMAGES_DICT)
                                train_deck_sprite.update(draw=True)
                                mini_cards_sprites.update(draw=True)
                        if destination:
                            if destination not in clicked_destination_button_sprites.sprites():
                                clicked_destination_button_sprites.add(destination)
                            else:
                                clicked_destination_button_sprites.remove(destination)

                            destination_button_sprites.update(color=DESTINATION_COLOR)
                            clicked_destination_button_sprites.update(
                                color=(DESTINATION_COLOR[0] - 30, DESTINATION_COLOR[1] - 30,
                                       DESTINATION_COLOR[2] - 30))
                            if len(clicked_destination_button_sprites.sprites()) >= minimum_destination_cards:
                                chosen_destination_button_sprite.update(color=BUTTON_COLOR)
                            else:
                                chosen_destination_button_sprite.update(delete=True)

                    elif turn_action:
                        train_card = None
                        destination_cards = []
                        mini_card = None

                        if not clicked_route_claiming_cards_sprites.sprites():
                            train_card, draws_left = train_card_click(game, event.pos, draws_left, train_deck_sprite,
                                                                      train_cards_action_sprites)
                            destination_cards = destination_deck_click(game, event.pos, destination_deck_sprite,
                                                                       destination_cards)
                            if draws_left == 2:
                                mini_card = mini_card_click(event.pos, game, mini_cards_sprites,
                                                            clicked_route_claiming_cards_sprites)
                        else:
                            mini_card = mini_card_click(event.pos, game, mini_cards_sprites,
                                                        clicked_route_claiming_cards_sprites)

                        if destination_cards:
                            choosing_destinations = True
                            turn_action = False
                            destination_cards = game.draw_destination_cards()
                            destination_button_sprites.update(color=DESTINATION_COLOR)
                            choose_destination_cards_text = Text(
                                f"Choose a minimum of {minimum_destination_cards} cards", (0, 0, 0),
                                BIG_TEXT_SIZE, screen.get_width() / 2, screen.get_height() / 2 - BIG_TEXT_SIZE,
                                center=True)
                            destination_button_text_sprite.add(choose_destination_cards_text)
                        elif train_card:
                            draw_mini_numbers(screen, game.get_current_player(), mini_numbers_sprites,
                                              all_game_turn_sprites,
                                              mini_cards_sprites.sprites()[0].rect.width)
                            turn_face_up_cards(game, train_cards_action_sprites, TRAIN_IMAGES_DICT)
                            if draws_left == 0:
                                game.next_turn()
                                switch_player_text(screen, game, board, current_player_text_sprite)
                                draws_left = 2
                                destination_deck_sprite.update(draw=True)
                                train_deck_sprite.update(draw=True)
                                mini_cards_sprites.update(draw=True)
                            pass
                        elif mini_card:
                            add_to_clicked_route_claiming_cards_sprites(mini_card,
                                                                        clicked_route_claiming_cards_sprites,
                                                                        route_claiming_cards_sprites)
                            # image_name = railway_click(event.pos, railway_masks)
                            # if image_name:
                            #    board = board_with_masks(screen, board, railway_images[image_name])
                        elif clicked_route_claiming_cards_sprites.sprites():
                            pass
                else:
                    for i in range(len(button_sprites.sprites())):
                        if button_sprites.sprites()[i].rect.collidepoint(event.pos):
                            create_players(game, i + 2)
                            game.started = True
                            choosing_destinations = True
                            button_sprites.update(delete=True)
                            button_sprites.draw(screen)
                            current_player_text = Text(game.get_current_player().color,
                                                       COLORS_DICT[game.get_current_player().color], BIG_TEXT_SIZE,
                                                       board.get_width() + BOARD_POSITION[0] + 20,
                                                       BOARD_POSITION[1])
                            current_player_text_sprite.add(current_player_text)
                            break

        if game.started:
            if choosing_destinations:
                screen.blit(board_cover, BOARD_POSITION)
                all_game_turn_sprites.update(delete=True)
                all_game_turn_sprites.draw(screen)
                destination_button_text_sprite.draw(screen)
                draw_destination_cards(destination_cards, screen, destination_button_sprites)
                chosen_destination_button_sprite.draw(screen)

            else:
                train_cards_action_sprites.draw(screen)
                destination_deck_sprite.draw(screen)
                train_deck_sprite.draw(screen)
                screen.blit(board, BOARD_POSITION)
                draw_scores_text(game, board, scores_text_sprites, screen, all_game_turn_sprites)
                draw_chosen_destinations_text(game, board, chosen_destinations_text_sprites, screen,
                                              all_game_turn_sprites)
                mini_cards_sprites.draw(screen)
                draw_mini_numbers(screen, game.get_current_player(), mini_numbers_sprites, all_game_turn_sprites,
                                  mini_cards_sprites.sprites()[0].rect.width)
                route_claiming_cards_sprites.draw(screen)
            current_player_text_sprite.draw(screen)
        else:
            button_sprites.draw(screen)
        pg.display.update()
        clock.tick(60)


def add_to_clicked_route_claiming_cards_sprites(card, clicked_route_claiming_cards_sprites,
                                                route_claiming_cards_sprites):
    for sprite in route_claiming_cards_sprites.sprites():
        if not sprite.color:
            sprite.update(color=card.color, image_path=TRAIN_IMAGES_DICT[card.color])
            clicked_route_claiming_cards_sprites.add(sprite)
            break


def draw_mini_numbers(screen, player, mini_numbers_sprites, all_game_turn_sprites, mini_width):
    mini_numbers_sprites.update(delete=True)
    mini_numbers_sprites.draw(screen)
    mini_numbers_sprites.empty()
    cards_dict = {i: 0 for i in TRAIN_COLORS_LIST}
    if player.cards:
        for card in player.cards:
            cards_dict[card] += 1
    for color in cards_dict:
        text = Text(str(cards_dict[color]), (0, 0, 0), MINI_TEXT_SIZE,
                    BOARD_POSITION[0] + 250 + TRAIN_COLORS_LIST.index(color) * (mini_width + 10) + mini_width / 2,
                    screen.get_height() - BOARD_POSITION[1] - MINI_TEXT_SIZE)
        mini_numbers_sprites.add(text)
    mini_numbers_sprites.draw(screen)
    all_game_turn_sprites.add(mini_numbers_sprites)


def draw_scores_text(game, board, scores_text_sprites, screen, all_game_turn_sprites):
    scores_text_sprites.update(delete=True)
    scores_text_sprites.draw(screen)
    scores_text_sprites.empty()
    for player in game.players:
        text = Text(f"{player.color}: {player.points}", COLORS_DICT[player.color], SMALL_TEXT_SIZE,
                    BOARD_POSITION[0] + 20 + board.get_width(),
                    BIG_TEXT_SIZE + 20 + (BOARD_POSITION[1] + SMALL_TEXT_SIZE) * game.players.index(player))
        scores_text_sprites.add(text)
    scores_text_sprites.draw(screen)
    all_game_turn_sprites.add(scores_text_sprites)


def draw_chosen_destinations_text(game, board, chosen_destinations_text_sprites, screen, all_game_turn_sprites):
    chosen_destinations_text_sprites.update(delete=True)
    chosen_destinations_text_sprites.draw(screen)
    chosen_destinations_text_sprites.empty()
    for destination in game.get_current_player().destination_cards:
        text = Text(str(destination), (0, 0, 0), MINI_TEXT_SIZE,
                    BOARD_POSITION[0], BOARD_POSITION[1] + board.get_height() +
                    MINI_TEXT_SIZE * game.get_current_player().destination_cards.index(destination))
        chosen_destinations_text_sprites.add(text)
    chosen_destinations_text_sprites.draw(screen)
    all_game_turn_sprites.add(chosen_destinations_text_sprites)


def turn_face_up_cards(game, train_cards_action_sprites, train_images_dict):
    for card, face_up_card in zip(game.face_up_cards, train_cards_action_sprites.sprites()):
        face_up_card.update(color=card, image_path=train_images_dict[card])


def switch_player_text(screen, game, board, current_player_text_sprite):
    current_player_text_sprite.update(delete=True)
    current_player_text_sprite.draw(screen)
    current_player_text = Text(game.get_current_player().color,
                               COLORS_DICT[game.get_current_player().color], BIG_TEXT_SIZE,
                               BOARD_POSITION[0] + board.get_width() + 20,
                               BOARD_POSITION[1])
    current_player_text_sprite.add(current_player_text)


def draw_destination_cards(destination_cards, screen, destination_button_sprites):
    for button, card in zip(destination_button_sprites.sprites(), destination_cards):
        button.add_text(str(card), SMALL_TEXT_SIZE, 40)
    destination_button_sprites.draw(screen)


def mini_card_click(event_pos, game, mini_cards_sprites, clicked_route_claiming_cards_sprites, ):
    if len(clicked_route_claiming_cards_sprites.sprites()) <= ROUTE_MAX_LENGTH:
        for card in mini_cards_sprites.sprites():
            if card.rect.collidepoint(event_pos):
                if card.color in game.get_current_player().cards:
                    game.get_current_player().remove_card(card.color)
                    return card
    return None


def train_card_click(game, event_pos, draws_left, train_deck_sprite, train_cards_action_sprites):
    if len(train_cards_action_sprites.sprites()) < 5:
        print(len(train_cards_action_sprites.sprites()))
        return None, draws_left
    if train_deck_sprite.sprite.rect.collidepoint(event_pos):
        train_card = game.draw_card()
        game.get_current_player().add_card(train_card)
        return train_card, draws_left - 1
    else:
        for card in train_cards_action_sprites.sprites():
            if card.rect.collidepoint(event_pos):
                if draws_left == 2 or (draws_left == 1 and card.color != ANY_COLOR):
                    print(game.turn, card.color, len(train_cards_action_sprites.sprites()))
                    game.draw_card(card.color)
                    game.get_current_player().add_card(card.color)
                    if card.color == ANY_COLOR:
                        return card.color, draws_left - 2
                    return card.color, draws_left - 1
    print(len(train_cards_action_sprites.sprites()), "no clickies")
    return None, draws_left


def destination_deck_click(game, event_pos, destination_deck_sprite, destination_cards):
    if destination_deck_sprite.sprite.rect.collidepoint(event_pos):
        destination_cards = game.draw_destination_cards()
        return destination_cards
    return destination_cards


def destination_click(event_pos, destination_button_sprites):
    for button in destination_button_sprites.sprites():
        if button.rect.collidepoint(event_pos):
            return button


def choose_destination_click(event_pos, button):
    if button.rect.collidepoint(event_pos):
        return True


def railway_click(event_pos, masks):
    for key in masks:
        if is_click_inside_mask(event_pos, masks[key]):
            return key


def is_click_inside_mask(click_pos, mask):
    try:
        relative_pos = (click_pos[0] - BOARD_POSITION[0], click_pos[1] - BOARD_POSITION[1])
        return mask.get_at(relative_pos)
    except IndexError:
        return False


def board_with_masks(screen, board, mask_image):
    result_image = pg.Surface(board.get_size())
    result_image = result_image.convert_alpha()
    result_image.fill((255, 255, 255))
    result_image.blit(mask_image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

    return result_image


if __name__ == '__main__':
    main()
