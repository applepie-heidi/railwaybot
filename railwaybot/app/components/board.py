import pygame as pg


class Board(pg.sprite.Sprite):
    def __init__(self, image_path, x, y, railway_images):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_path)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.railway_images = railway_images

    def add_mask(self, mask):
        result_image = pg.Surface(self.image.get_size())
        result_image = result_image.convert_alpha()
        result_image.fill((255, 255, 255))
        result_image.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.image.blit(result_image, (0, 0))


class BoardGroup(pg.sprite.GroupSingle):
    def __init__(self):
        super().__init__()
        self.clicked_railway = None

    def add(self, *boards: Board):
        super().add(*boards)

    def handle_click(self, pos):
        for image_name in self.sprite.railway_images:
            try:
                relative_pos = (pos[0] - self.sprite.rect.x, pos[1] - self.sprite.rect.y)
                mask = pg.mask.from_surface(self.sprite.railway_images[image_name])
                if mask.get_at(relative_pos):
                    self.sprite.add_mask(self.sprite.railway_images[image_name])
                    self.clicked_railway = image_name
            except IndexError:
                pass

    def remove_clicked_railway(self):
        self.clicked_railway = None

    def get_clicked_railway(self):
        return self.clicked_railway
