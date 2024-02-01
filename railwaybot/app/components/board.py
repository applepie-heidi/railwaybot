from __future__ import annotations

import pygame as pg

from engine.board import Railway
from engine.game import Game


def replace_color(image, old_color, new_color):
    pixels = pg.PixelArray(image)
    pixels.replace(old_color, new_color)
    del pixels


class Board(pg.sprite.Sprite):
    def __init__(self, image_path, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_path)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def add_mask(self, mask):
        result_image = pg.Surface(self.image.get_size())
        result_image = result_image.convert_alpha()
        result_image.fill((255, 255, 255))
        result_image.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.image.blit(result_image, (0, 0))


class BoardGroup(pg.sprite.GroupSingle):
    sprite: Board

    def __init__(self, game: Game, colors_dict, image_path, x, y):
        super().__init__()
        self.game = game
        self.colors_dict = colors_dict
        self.railway_images = {}  # type: dict[tuple[str,str,str], pg.Surface]
        self.clicked_railway = None  # type: tuple[str,str,str] | None
        self.board = Board(image_path, x, y)
        self.add(self.board)

    def add(self, *boards: Board):
        super().add(*boards)

    @classmethod
    def from_finished_game(cls, game: Game, railway_images, colors_dict, image_path, x, y):
        bg = cls(game, colors_dict, image_path, x, y)
        # bg.set_railway_images(railway_images)
        for player in game.players:
            for railway in player.claimed_railways:  # type: Railway
                x_str = "x" if railway.is_x else ""
                railway_tuple = (railway.city1, railway.city2, railway.color + x_str)
                image = railway_images[railway_tuple]
                replace_color(image, (0, 0, 0), colors_dict[player.color])
                bg.sprite.add_mask(image)

        return bg

    def handle_click(self, pos):
        for railway, image in self.railway_images.items():
            try:
                relative_pos = (pos[0] - self.sprite.rect.x, pos[1] - self.sprite.rect.y)
                mask = pg.mask.from_surface(image)
                if mask.get_at(relative_pos):
                    player_color = self.game.get_current_player().color
                    replace_color(image, (0, 0, 0), self.colors_dict[player_color])
                    self.sprite.add_mask(image)
                    self.clicked_railway = railway
                    break
            except IndexError:
                pass

    def remove_clicked_railway(self):
        self.clicked_railway = None

    def get_clicked_railway(self):
        return self.clicked_railway

    def set_railway_images(self, railway_images):
        self.railway_images = railway_images
