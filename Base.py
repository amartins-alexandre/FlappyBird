"""
The Base class is responsible for the base of the game screen where the bird moves. It is a simple image that moves
from right to left to give the illusion that the bird is moving forward.
The Base class has the following attributes:
    BASE_IMAGE: The image of the base.
    VEL: The velocity at which the base moves.
    WIDTH: The width of the base image.
    IMG: The image of the base.
"""

import os

import pygame


class Base:
    BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")))
    VEL = 5
    WIDTH = BASE_IMAGE.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        # self.height = self.BASE_IMAGE.get_height()

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.BASE_IMAGE, (self.x1, self.y))
        screen.blit(self.BASE_IMAGE, (self.x2, self.y))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        base_mask = pygame.mask.from_surface(self.BASE_IMAGE)

        base_offset = (self.x1 - bird.x, self.y - round(bird.y))

        return bird_mask.overlap(base_mask, base_offset) is not None
