import pygame

from Config import C_WIN_WIDTH


class Overlay:

    def __init__(self):
        self.score = 0
        self.gen = 0
        self.alive = 10

    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 50)
        score = font.render("Score: " + str(self.score), True, (255, 255, 255))
        generation = font.render("Gen: : " + str(self.gen), True, (255, 255, 255))
        alive = font.render("Alive: " + str(self.alive), True, (255, 255, 255))

        win.blit(score, (C_WIN_WIDTH - 10 - score.get_width(), 10))
        win.blit(generation, (10, 10))
        win.blit(alive, (10, 45))
