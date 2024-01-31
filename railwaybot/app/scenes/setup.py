from app.scenes.scene import Scene


class SetupScene(Scene):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.number_of_players = 0
        self.player_towns = []
        self.scene = NumberOfPlayersScene(game)

    def handle_click(self, pos):
        self.scene.handle_click(pos)
        if self.game.players:  # imamo samo ako je prethodna scena napravila igrače
            self.scene = DestinationChooserScene(game)

    def draw(self, screen):
        self.scene.draw(screen)

    @property
    def is_finished(self):
        return bool(self.game.players) and all(player.towns for player in self.game.players)
