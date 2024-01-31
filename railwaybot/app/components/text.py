import pygame as pg
from app.config import *


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


class TextGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()

    def add(self, *texts: Text):
        super().add(*texts)
