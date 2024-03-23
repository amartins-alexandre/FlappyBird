"""
The Bird class is a new class that will represent the bird that the player controls.
It has the following class variables:
    BIRDS_IMG: A list of images of the bird. The bird has three images:
        - one with its wings up;
        - one with its wings down;
        - and one with its wings in the middle.
    MAX_ROTATION: The maximum rotation of the bird.
    ROT_VEL: The velocity at which the bird rotates.
    ANIMATION_TIME: The time it takes to change the bird's image.
"""
import os

import pygame


class Bird:
    BIRDS_IMG = [
        pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird1.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird2.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird2.png"))),
    ]
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.tick_count = 0
        self.image = self.BIRDS_IMG[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # Calculate displacement
        shift = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        if shift >= 16:
            shift = 16

        if shift < 0:
            shift -= 2

        self.y += shift

        # If the bird is moving up, tilt it upwards
        if shift < 0 or self.y < (self.height + 50):
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
            else:
                if self.tilt > -90:
                    self.tilt -= self.ROT_VEL
        else:
            if self.tilt < 25:
                self.tilt += self.ROT_VEL

    def draw(self, screen):
        # Update the image of the bird
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.image = self.BIRDS_IMG[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.image = self.BIRDS_IMG[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.image = self.BIRDS_IMG[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.image = self.BIRDS_IMG[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.image = self.BIRDS_IMG[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.image = self.BIRDS_IMG[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Rotate the bird
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
