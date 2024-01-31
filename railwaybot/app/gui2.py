from __future__ import annotations

import pygame as pg

from app.scenes.dest import DestinationChooserScene
from app.scenes.main import MainScene


def main():
    pg.init()
    screen = pg.display.set_mode((1300, 1000), pg.SCALED)
    pg.display.set_caption("Ticket to Ride")

    screen.fill((255, 255, 255))

    clock = pg.time.Clock()

    done = False
    scene1 = DestinationChooserScene(None, "red", ["City 1", "City 2", "City 3"])
    scene2 = DestinationChooserScene(None, "green", ["Grad 1", "Grad 2", "Grad 3"])
    main_scene = MainScene(None)

    current_scene = scene1

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if current_scene:
                    current_scene.handle_click(event.pos)

            if current_scene and current_scene.is_finished:
                # Switch to the next scene
                # TODO: Definition of "next" remains to be defined
                if current_scene is scene1:
                    current_scene = scene2
                elif current_scene is scene2:
                    current_scene = main_scene

        if done:
            break

        current_scene and current_scene.draw(screen)
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
