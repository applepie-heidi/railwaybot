from app.scenes.dest import DestinationChooserScene
from app.scenes.playernum import NumberOfPlayersScene
from app.scenes.scene import Scene
from app.config import CARDS_DRAW_INITIAL


class SetupScene(Scene):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.number_of_players = 0
        self.player_towns = []
        self.scene = NumberOfPlayersScene(game)

    def handle_click(self, pos):
        self.scene.handle_click(pos)
        if self.game.players:
            if type(self.scene) is NumberOfPlayersScene:
                self.scene = DestinationChooserScene(self.game)
            elif self.scene.is_finished():
                for player in self.game.players:
                    for i in range(CARDS_DRAW_INITIAL):
                        player.add_card(self.game.draw_card())

    def draw(self, screen):
        self.scene.draw(screen)

    @property
    def is_finished(self):
        return bool(self.game.players) and all(player.towns for player in self.game.players)
