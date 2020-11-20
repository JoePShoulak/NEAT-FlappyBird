import os

import pygame

pygame.font.init()


def load_image(img):
    image_location = os.path.join("imgs", img)
    image = pygame.image.load(image_location)
    return pygame.transform.scale2x(image)


BG_IMG = load_image("bg.png")


def draw_window(win, birds, pipes, base, overlay):
    win.blit(BG_IMG, (0, 0))

    for bird in birds:
        bird.draw(win)

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    overlay.draw(win)

    pygame.display.update()
