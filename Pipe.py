"""
The Pipe class is a new class that will represent the pipes that the bird has to avoid. It has three class variables:
    PIPE_IMAGE: The image of the pipe.
    GAP: The gap between the top and bottom pipes.
    VEL: The velocity at which the pipes move to the left.
"""

import os
import random

import pygame


class Pipe:
    PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "pipe.png")))
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.pipe_top_position = 0
        self.pipe_bottom_position = 0
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMAGE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randint(50, 450)
        self.pipe_top_position = self.height - self.PIPE_TOP.get_height()
        self.pipe_bottom_position = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.pipe_top_position))
        screen.blit(self.PIPE_BOTTOM, (self.x, self.pipe_bottom_position))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.pipe_top_position - round(bird.y))
        bottom_offset = (self.x - bird.x, self.pipe_bottom_position - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        return True if top_point or bottom_point else False
