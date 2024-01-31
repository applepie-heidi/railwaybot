import pygame as pg


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

    def _blit_text(self):
        font = pg.font.Font(None, self.text_size)
        text_image = font.render(self.text, True, (0, 0, 0))
        text_pos = text_image.get_rect(centerx=self.image.get_width() / 2, y=self.text_y)
        self.image.blit(text_image, text_pos)

class PlayerNumberButtonGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.selected = []

    def add(self, *buttons: Button):
        # TODO Find the corrent position and update the button rect
        super().add(*buttons)

    def handle_click(self, pos):
        for button in self.sprites():
            if button.rect.collidepoint(pos):
                print("Clicked:", button.text)
                button.toggle()
                if button.checked:
                    self.selected.append(button)
                else:
                    self.selected.remove(button)

    def get_selected(self):
        return self.selected