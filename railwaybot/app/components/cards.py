import pygame as pg


class Card(pg.sprite.Sprite):
    def __init__(self, image_path, x, y, width, height, color=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color


class DeckGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self._clicked = False

    def add(self, *cards: Card):
        super().add(*cards)

    def handle_click(self, pos):
        for card in self.sprites():
            if card.rect.collidepoint(pos):
                self._clicked = True

    def unclick(self):
        self._clicked = False

    @property
    def is_clicked(self):
        return self._clicked
