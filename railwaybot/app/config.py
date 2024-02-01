import json
import os
import random
import engine.game

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
MAX_PLAYERS = len(COLORS_DICT)
TRAIN_IMAGES_DICT = parse_train_images()
TRAIN_COLORS_LIST = get_shuffled_colors(TRAIN_IMAGES_DICT)
SCREEN_SIZE = (1300, 1000)
SCREEN_COLOR = (220, 216, 215)
BUTTON_COLOR = (141, 54, 34)
DESTINATION_COLOR = (123, 147, 147)
BUTTON_SIZE_X = 100
CARD_VERTICAL_SIZE = (89, 137)
CARD_HORIZONTAL_SIZE = (137, 89)
MINI_CARD_SIZE = (82, 53)
BIG_TEXT_SIZE = 80
HUGE_TEXT_SIZE = 110
SMALL_TEXT_SIZE = 30
MINI_TEXT_SIZE = 20
BOARD_POSITION = (10, 10)
PADDING = 10
DESTINATION_SIZE = (350, 100)
DESTINATIONS_PADDING = 250
ROUTE_MAX_LENGTH = 6

CARDS_DRAW_INITIAL = 4
CARDS_DRAW = 2
MINIMUM_DESTINATION_CARDS_INITIAL = 2
MINIMUM_DESTINATION_CARDS = 1
ANY_COLOR = engine.game.ANY_COLOR