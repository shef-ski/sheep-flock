from typing import Any
from pygame import Color
from pygame import Vector2
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
    
    def move(self, sheep: list, dogs: list):
        # Random movement
        # Implement better movement tactics later
        new_velocity = Vector2(
            rand.uniform(-0.01,0.01),
            rand.uniform(-0.01,0.01)
        )
        self.velocity = new_velocity
        self.position += self.velocity 
    

class Sheep(Animal):
    def __init__(self,id, position, velocity):
        super().__init__(id, position, velocity, Color(0,255,0,255))

class Dog(Animal):
    def __init__(self, id, position, velocity):
        super().__init__(id, position, velocity, Color(0,0,255,255))