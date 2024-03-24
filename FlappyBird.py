import os

import pygame
import neat

from Base import Base
from Bird import Bird
from Pipe import Pipe

IA_PLAYING = True

WEIGHT_SCREEN = 500
HEIGHT_SCREEN = 800

# Load images
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bg.png")))

# Load sounds
pygame.font.init()
FONT = pygame.font.SysFont("arial", 50)


def draw_window(win, birds, pipes, base, score, gen):
    # Draw background
    win.blit(BG_IMAGE, (0, 0))

    # Draw birds
    for bird in birds:
        bird.draw(win)

    # Draw pipes
    for pipe in pipes:
        pipe.draw(win)

    # Draw base
    base.draw(win)

    # Draw score
    score_label = FONT.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(score_label, (WEIGHT_SCREEN - 10 - score_label.get_width(), 10))

    if IA_PLAYING:
        # Draw generation
        gen_label = FONT.render(f"Gen: {gen}", 1, (255, 255, 255))
        win.blit(gen_label, (10, 10))

    # Update display
    pygame.display.update()


def main(genomes, config):  # fitness function
    win = pygame.display.set_mode((WEIGHT_SCREEN, HEIGHT_SCREEN))
    clock = pygame.time.Clock()
    base = Base(730)
    pipes = [Pipe(600)]
    score = 0
    gen = 0

    birds = []
    networks = []
    genome_list = []
    if IA_PLAYING:
        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            networks.append(network)
            genome.fitness = 0
            genome_list.append(genome)
            birds.append(Bird(230, 350))
    else:
        birds = [Bird(230, 350)]

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if not IA_PLAYING and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for bird in birds:
                    bird.jump()

        # Get pipe index
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            break

        # Move base
        base.move()

        # Move birds
        for i, bird in enumerate(birds):
            bird.move()
            genome_list[i].fitness += 0.1
            output = networks[i].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom_position))
            )
            if output[0] > 0.5:
                bird.jump()

        # Move pipes
        add_pipe = False
        remove_pipe = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                    if IA_PLAYING:
                        genome_list[i].fitness -= 1
                        networks.pop(i)
                        genome_list.pop(i)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipe.append(pipe)

            pipe.move()

        for r in remove_pipe:
            pipes.remove(r)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
            if IA_PLAYING:
                for genome in genome_list:
                    genome.fitness += 5

        for i, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(i)
                if IA_PLAYING:
                    networks.pop(i)
                    genome_list.pop(i)

        if IA_PLAYING and score > 50:
            for genome in genome_list:
                genome.fitness += 10
                birds = []
                networks = []
                genome_list = []

        draw_window(win, birds, pipes, base, score, gen)


def run(config_path):
    if IA_PLAYING:
        config = neat.config.Config(neat.DefaultGenome,
                                    neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation,
                                    config_path)

        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())
        population.run(main, 50)
    else:
        main(None, None)


if __name__ == "__main__":
    config_feedforward = os.path.join(os.path.dirname(__file__), "config-feedforward.txt")
    run(config_feedforward)
