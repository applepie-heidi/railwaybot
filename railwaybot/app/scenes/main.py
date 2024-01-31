from typing import Optional

import pygame as pg

from app.scenes.scene import Scene


class RightStuffGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.two_buttons = []  # TODO na licu mjesta
        self.five_buttons = []  # TODO na licu mjesta

    def handle_click(self, pos):
        pass


class BottomStuffGroup(pg.sprite.Group):

    def handle_click(self, pos):
        pass


class MainScene(Scene):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.main_stuff = BottomStuffGroup()
        self.right_stuff = RightStuffGroup()
        self.bottom_stuff = BottomStuffGroup()

        self.sub_scene: Optional[Scene] = None

    def handle_click(self, pos):
        self.main_stuff.handle_click(pos)
        self.right_stuff.handle_click(pos)
        self.bottom_stuff.handle_click(pos)

        # if kliked_orange_shit:
        #     self.sub_scene = DestinationChooserScene(self.game, "red", ["City 1", "City 2", "City 3"])

    def draw(self, screen):
        if self.sub_scene is not None:
            self.sub_scene.draw(screen)
        else:
            self.main_stuff.draw(screen)
            self.right_stuff.draw(screen)
            self.bottom_stuff.draw(screen)

    @property
    def is_finished(self):
        return False
