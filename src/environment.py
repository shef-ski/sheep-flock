import numpy as np
import pygame
from pygame import Vector2, DOUBLEBUF
from animals.sheep import Sheep
from animals.dog import Dog
from utils import timed
import random as rand


class Environment:
    def __init__(self, dimensions, n_sheep, n_dogs):
        """
        dimensions -> tuple of (width, height)
        n_sheep -> number of sheep
        n_dogs -> number of dogs
        """

        self.mapW, self.mapH = dimensions
        self.n_sheep = n_sheep
        self.n_dogs = n_dogs
        self.herd = self._init_herd()
        self.dogs = self._init_dogs()

        pygame.init()
        pygame.display.set_caption("Sheep herding")
        self.canvas = pygame.display.set_mode((self.mapW, self.mapH), DOUBLEBUF)
        self.canvas.set_alpha(None)
        self.fps = pygame.time.Clock()
        self.translation_vector = Vector2(self.mapW/2, self.mapH/2)
    
    def _translate_to_canvas(self, vector: Vector2):
        translated = vector + Vector2(1,1)
        translated.x *= self.mapW/2
        translated.y *= self.mapH/2
        return translated

    def _init_herd(self) -> list[Sheep]:
        sheep = []

        mean = [0, 0]
        cov = np.array([[0.1, 0],  # Variance for x and y (diagonal values)
                        [0, 0.1]])  # Small values keep the points near the center

        for i in range(self.n_sheep):
            x, y = np.random.multivariate_normal(mean, cov)
            position = Vector2(float(x), float(y))

            velocity = Vector2(
                rand.uniform(-0.1, 0.1),
                rand.uniform(-0.1, 0.1)
            )
            sheep.append(Sheep(i, position, velocity))
        return sheep
    
    def _init_dogs(self) -> list[Dog]:
        dogs = []
        for i in range(self.n_dogs):
            position = Vector2(
                rand.uniform(-1, 1),
                rand.uniform(-1, 1)
            )

            velocity = Vector2(
                rand.uniform(-0.1, 0.1),
                rand.uniform(-0.1, 0.1)
            )
            dogs.append(Dog(i, position, velocity))
        return dogs

    def _choose_sheep_to_excite(self, p):
        """
        With probability p, select a (uniformly) random sheep in the herd which becomes excited.
        """
        if rand.random() < p:
            chosen_sheep = rand.choice(self.herd)
            chosen_sheep.excite()

    @timed
    def update_animals(self):
        # Create copies of sheep/dogs so that we update them at the same time
        # This is probably very inefficient, should be replaced with something
        # else later
        herd_copy = self.herd.copy()
        dogs_copy = self.dogs.copy()

        p_excited = 0.002
        self._choose_sheep_to_excite(p_excited)
        
        for sheep in self.herd:
            sheep.move(herd_copy, dogs_copy)
        
        for dog in self.dogs:
            dog.move(herd_copy, dogs_copy)

    def draw(self):
        self.canvas.fill((255,255,255))
        for i, sheep in enumerate(self.herd):
            pygame.draw.circle(
                self.canvas,
                sheep.color,
                self._translate_to_canvas(sheep.position),
                self.mapW / 100
            )
            
        for dog in self.dogs:
            pygame.draw.circle(
                self.canvas,
                dog.color,
                self._translate_to_canvas(dog.position),
                self.mapW / 100
            )

        self.update_animals()
        pygame.display.update()
        self.fps.tick(60)
        