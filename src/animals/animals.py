import os

from pygame import Color
from pygame import Vector2
from src.utils import timed
import random as rand

class Animal:
    def __init__(self,
        id:int,
        position:Vector2,
        velocity:Vector2,
        color:Color,
    ):
        """
        Initializes the position, velocity and color of the animal
        Position -> 2d vector representing the x & y coordinates
        Velocity -> 2d vector representing the movement vector of the sheep
        Color -> The color used to draw the animal
        """
        self.id = id
        self.position = position
        self.velocity = velocity
        self.color = color
        self.observation_radius = float(os.getenv('ANIMAL_OBSERVATION_RADIUS'))
        self.dog_observation_radius = float(os.getenv('DOG_OBSERVATION_RADIUS'))


    @timed
    def find_neighbors(self, sheep: list, dogs: list):
        # right now only sheep relevant we may need to change this method to be type aware
        return  [
            other for other in sheep
            if other.id != self.id and (self.position - other.position).magnitude() <= self.observation_radius
        ]

    @timed
    def find_neighbors_dog(self, sheep: list, dogs: list):
        # right now only sheep relevant we may need to change this method to be type aware
        return [
            other for other in sheep
            if other.id != self.id and (self.position - other.position).magnitude() <= self.dog_observation_radius
        ]

