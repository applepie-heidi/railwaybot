import json
import os
import random

import pygame as pg
from pygame import PixelArray

from engine.game import Game, Player


def parse_player_json():
    with open(PLAYER_JSON, "r") as f:
        data = json.load(f)
        colors = {}
        for color in data["colors"]:
            colors[color["name"]] = (color["r"], color["g"], color["b"])
        return colors, data["trains_per_player"]


def get_shuffled_colors(colors):
    shuffled_colors = []
    for color in colors:
        shuffled_colors.append(color)
    random.shuffle(shuffled_colors)
    return shuffled_colors


BOARD_FILENAME = "data/jsons/board.json"
DESTINATION_CARDS_FILENAME = "data/jsons/destination_cards.json"
TRAIN_CARDS_FILENAME = "data/jsons/train_cards.json"
SCORING_FILENAME = "data/jsons/scoring.json"
PLAYER_JSON = "data/jsons/player.json"
RAILWAY_IMAGES_DIRECTORY = "data/images/railways"
BOARD_IMAGE_FILENAME = "data/images/board.png"
BOARD_POSITION = (10, 10)
COLORS_DICT, TRAINS = parse_player_json()
COLORS_LIST = get_shuffled_colors(COLORS_DICT)
SCREEN_COLOR = (220, 216, 215)
BUTTON_COLOR = (141, 54, 34)
BUTTON_SIZE_X = 100
BIG_TEXT_SIZE = 100


class Button(pg.sprite.Sprite):
    def __init__(self, color, width, height, text, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        text_pos = text.get_rect(centerx=self.image.get_width() / 2, y=15)
        self.image.blit(text, text_pos)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.image.fill(SCREEN_COLOR)


class Text(pg.sprite.Sprite):
    def __init__(self, text, color, size, x, y):
        pg.sprite.Sprite.__init__(self)
        font = pg.font.Font(None, size)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.image.get_width() / 2
        self.rect.y = y

    def update(self):
        self.image.fill(SCREEN_COLOR)


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


def load_image(path, color_key=None):
    image = pg.image.load(path)
    image = image.convert_alpha()
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


def create_buttons(button_position):
    button_position_x = button_position[0] - 4 * (BUTTON_SIZE_X + 10)
    button_position_y = button_position[1]
    buttons = []
    font = pg.font.Font(None, BUTTON_SIZE_X)
    button_sprites = pg.sprite.Group()
    for i in range(2, len(COLORS_DICT) + 1):
        button = Button(BUTTON_COLOR, BUTTON_SIZE_X, BUTTON_SIZE_X, font.render(str(i), True, (0, 0, 0)),
                        button_position_x + i * (BUTTON_SIZE_X + 10), button_position_y)
        button_sprites.add(button)
        buttons.append(button)
    return button_sprites, buttons


def current_player_text(text):
    font = pg.font.Font(None, 36)
    return font.render(text, True, (0, 0, 0))


def main():
    pg.init()
    screen = pg.display.set_mode((1400, 900), pg.SCALED)
    pg.display.set_caption("Ticket to Ride")

    screen.fill(SCREEN_COLOR)

    game = Game(BOARD_FILENAME, DESTINATION_CARDS_FILENAME, TRAIN_CARDS_FILENAME, SCORING_FILENAME)

    choose_button_text = Text("Choose the number of players", (0, 0, 0), BIG_TEXT_SIZE, screen.get_width() / 2,
                              screen.get_height() / 2 - BIG_TEXT_SIZE)
    button_sprites, buttons = create_buttons((screen.get_width() / 2, screen.get_height() / 2))
    button_sprites.add(choose_button_text)

    board = load_image(BOARD_IMAGE_FILENAME)

    railway_images = load_railway_images(RAILWAY_IMAGES_DIRECTORY)
    railway_masks = {}
    for image_name in railway_images:
        choice = random.choice(COLORS_LIST)
        replace_color(railway_images[image_name], (0, 0, 0), COLORS_DICT[choice])
        railway_masks[image_name] = pg.mask.from_surface(railway_images[image_name])

    clock = pg.time.Clock()
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if game.started:
                    image_name = mouse_button_down(event.pos, railway_masks)
                    if image_name:
                        board = board_with_masks(screen, board, railway_images[image_name])
                else:
                    for i in range(len(buttons)):
                        if buttons[i].rect.collidepoint(event.pos):
                            create_players(game, i + 2)
                            game.started = True
                            button_sprites.update()
                            button_sprites.draw(screen)
                            print(game.players)
                            break

        if game.started:
            screen.blit(board, BOARD_POSITION)
        else:
            button_sprites.draw(screen)
        pg.display.update()
        clock.tick(60)


def mouse_button_down(event_pos, masks):
    for key in masks:
        if is_click_inside_mask(event_pos, masks[key]):
            return key


def is_click_inside_mask(click_pos, mask):
    relative_pos = (click_pos[0] - BOARD_POSITION[0], click_pos[1] - BOARD_POSITION[1])
    return mask.get_at(relative_pos)


def board_with_masks(screen, board, mask_image):
    result_image = pg.Surface(board.get_size())
    result_image = result_image.convert_alpha()
    result_image.fill((255, 255, 255))
    result_image.blit(mask_image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

    return result_image


if __name__ == '__main__':
    main()
