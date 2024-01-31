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


class ToggleButton(pg.sprite.Sprite):
    def __init__(self, color, width, height, x, y, text=None, text_size=0, text_y=0, checked=False):
        super().__init__()
        self.color = color
        self.image = pg.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.text = text
        self.text_size = text_size
        self.text_y = text_y
        if self.text:
            self._blit_text()
        self.checked = checked
        self.rect.x = x
        self.rect.y = y

    def _blit_text(self):
        font = pg.font.Font(None, self.text_size)
        text_image = font.render(self.text, True, (0, 0, 0))
        text_pos = text_image.get_rect(centerx=self.image.get_width() / 2, y=self.text_y)
        self.image.blit(text_image, text_pos)

    def set_checked(self, checked):
        self.checked = checked
        if self.checked:
            self.image.fill((self.color[0] - 30, self.color[1] - 30, self.color[2] - 30))
            if self.text:
                self._blit_text()
        else:
            self.image.fill(self.color)
            if self.text:
                self._blit_text()

    def toggle(self):
        self.set_checked(not self.checked)


class PlayerNumberButtonGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.clicked = None

    def add(self, *buttons: Button):
        super().add(*buttons)

    def handle_click(self, pos):
        for button in self.sprites():
            if button.rect.collidepoint(pos):
                self.clicked = button.text

    def get_clicked_text(self):
        return self.clicked


class ToggleButtonGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.selected = []

    def add(self, *buttons: ToggleButton):
        super().add(*buttons)

    def handle_click(self, pos):
        for button in self.sprites():
            if button.rect.collidepoint(pos):
                button.toggle()
                if button.checked:
                    self.selected.append(button)
                else:
                    self.selected.remove(button)

    def get_selected(self):
        return self.selected


class OkButtonGroup(pg.sprite.GroupSingle):
    def __init__(self):
        super().__init__()
        self._clicked = False

    def add(self, *buttons: Button):
        super().add(*buttons)

    def handle_click(self, pos):
        if self.sprite.rect.collidepoint(pos):
            self._clicked = True

    @property
    def is_clicked(self):
        return self._clicked
