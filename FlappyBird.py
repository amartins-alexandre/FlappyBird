import pygame
import os
import random

from Base import Base
from Bird import Bird
from Pipe import Pipe

WEIGHT_SCREEN = 500
HEIGHT_SCREEN = 800

# Load images
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bg.png")))

# Load sounds
pygame.font.init()
FONT = pygame.font.SysFont("arial", 50)


def draw_window(win, birds, pipes, base, score):
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

    # Update display
    pygame.display.update()


def main():
    win = pygame.display.set_mode((WEIGHT_SCREEN, HEIGHT_SCREEN))
    clock = pygame.time.Clock()
    base = Base(730)
    pipes = [Pipe(600)]
    birds = [Bird(230, 350)]
    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        # Move base
        base.move()

        # Move birds
        for bird in birds:
            bird.move()

        # Move pipes
        add_pipe = False
        remove = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in remove:
            pipes.remove(r)

        for i, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(i)

        draw_window(win, birds, pipes, base, score)


if __name__ == "__main__":
    main()
