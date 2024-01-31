from __future__ import annotations

import pygame as pg

from app.scenes.dest import DestinationChooserScene
from app.scenes.main import MainScene
from app.scenes.setup import SetupScene
from app.config import *
from engine.game import Game


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
    pg.display.set_caption("Ticket to Ride")

    game = Game(BOARD_PATH, DESTINATION_CARDS_PATH, TRAIN_CARDS_PATH, SCORING_PATH)

    clock = pg.time.Clock()

    done = False
    main_scene = MainScene(game)

    current_scene = SetupScene(game)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if current_scene:
                    current_scene.handle_click(event.pos)

            if current_scene and current_scene.is_finished:
                if isinstance(current_scene, SetupScene):
                    current_scene = main_scene

        if done:
            break

        current_scene and current_scene.draw(screen)
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
