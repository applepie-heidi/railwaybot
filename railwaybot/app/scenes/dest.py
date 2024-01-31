from typing import List

from app.components.toggle import ToggleButtonGroup, ToggleButton
from app.scenes.scene import Scene


class DestinationChooserScene(Scene):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self._finished = False

        self.dest_group = ToggleButtonGroup()
        for name in self.names:
            self.dest_group.add(ToggleButton(name))
        # self.ok_button = Button("OK")

        self.odabrane_stvari = None

    def handle_click(self, pos):
        self.dest_group.handle_click(pos)
        # also handle ok button
        # Ako OK kliknut:
        # self._finished = True

    def draw(self, screen):
        self.dest_group.draw(screen)

    @property
    def is_finished(self):
        return self._finished
