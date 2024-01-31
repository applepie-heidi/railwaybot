from app.scenes.dest import DestinationChooserScene
from app.scenes.playernum import NumberOfPlayersScene
from app.scenes.scene import Scene
from app.config import *


class SetupScene(Scene):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.players_setup = 0
        self._finished = False
        self.scene = NumberOfPlayersScene(game)

    def handle_click(self, pos):
        self.scene.handle_click(pos)
        if isinstance(self.scene, NumberOfPlayersScene) and self.scene.is_finished:
            for player in self.game.players:
                for i in range(CARDS_DRAW_INITIAL):
                    player.add_card(self.game.draw_card())
            destinations = self.game.draw_destination_cards()
            self.scene = DestinationChooserScene(self.game, destinations, MINIMUM_DESTINATION_CARDS_INITIAL,
                                                 current_player=self.game.players[self.players_setup])
        elif isinstance(self.scene, DestinationChooserScene) and self.scene.is_finished:
            self.players_setup += 1
            if self.players_setup == len(self.game.players):
                self._finished = True
            else:
                destinations = self.game.draw_destination_cards()
                self.scene = DestinationChooserScene(self.game, destinations, MINIMUM_DESTINATION_CARDS_INITIAL,
                                                     current_player=self.game.players[self.players_setup])

    def draw(self, screen):
        self.scene.draw(screen)

    @property
    def is_finished(self):
        return self._finished
