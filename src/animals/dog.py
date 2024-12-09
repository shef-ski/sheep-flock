from pygame import Color, Vector2

from src.animals.animals import Animal
import random as rand

class Dog(Animal):
    def __init__(self, id, position, velocity):
        super().__init__(id, position, velocity, Color(0,0,255,255))

    def move(self, sheep: list, dogs: list):
        # Random movement
        # Implement better movement tactics later
        new_velocity = Vector2(
            rand.uniform(-0.01, 0.01),
            rand.uniform(-0.01, 0.01)
        )
        self.velocity = new_velocity
        self.position += self.velocity