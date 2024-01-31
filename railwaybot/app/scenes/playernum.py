from app.scenes.scene import Scene


class NumberOfPlayersScene(Scene):
    def __init__(self, game):
        super().__init__()
        self.game = game

