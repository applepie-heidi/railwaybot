import pygame as pg


class ToggleButton(pg.sprite.Sprite):
    def __init__(self, text, checked=False):
        super().__init__()
        # Sprite props
        self.image = pg.Surface((50, 50))
        self.rect = self.image.get_rect()

        # My props
        self.text = text
        self.checked = checked

    def set_checked(self, checked):
        self.checked = checked
        if self.checked:
            self.image.fill((0, 0, 0))
        else:
            self.image.fill((0, 255, 0))

    def toggle(self):
        self.set_checked(not self.checked)


class ToggleButtonGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.selected = []

    def add(self, *buttons: ToggleButton):
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

