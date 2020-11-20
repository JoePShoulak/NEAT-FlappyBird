import os
import pygame
import neat

from Classes.Base import Base
from Classes.Bird import Bird
from Classes.Pipe import Pipe
from Classes.Overlay import Overlay

from Helper import draw_window
from Config import C_WIN_HEIGHT, C_WIN_WIDTH, C_START_Y, C_START_X, C_BASE_HEIGHT, C_PIPE_DISTANCE, C_FPS, C_POP

gen = 0


def eval_genomes(genomes, config):
    global gen
    gen += 1

    birds = []
    nets = []
    ge = []

    for _, g in genomes:
        g.fitness = 0

        birds.append(Bird(C_START_X, C_START_Y))
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        ge.append(g)

    win = pygame.display.set_mode((C_WIN_WIDTH, C_WIN_HEIGHT))
    clock = pygame.time.Clock()

    base = Base(C_BASE_HEIGHT)
    pipes = [Pipe(C_PIPE_DISTANCE)]

    o = Overlay()
    o.gen = gen

    while True:
        clock.tick(C_FPS)
        base.move()

        o.alive = C_POP

        scored = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            break

        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += (1.0 / C_FPS)

            pipe_top_d = abs(bird.y - pipes[pipe_index].height)
            pipe_bot_d = abs(bird.y - pipes[pipe_index].bottom)

            output = nets[i].activate((bird.y, pipe_top_d, pipe_bot_d))

            if output[0] > 0.5:
                bird.jump()

        for i, bird in enumerate(birds):
            if bird.hit_ground() or bird.too_high():
                ge[i].fitness -= 1
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        for pipe in pipes:
            pipe.move()

            if pipe.offscreen():
                pipes.remove(pipe)

            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)

                if bird.passed(pipe):
                    scored = True

        if scored and len(pipes) == 1:
            o.score += 1
            pipes.append(Pipe(C_PIPE_DISTANCE))
            for g in ge:
                g.fitness += 5

        if o.score > 15:
            break

        o.alive = len(birds)
        draw_window(win, birds, pipes, base, o)


def run(path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                path)

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())

    winner = pop.run(eval_genomes, 50)
    print(winner)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
