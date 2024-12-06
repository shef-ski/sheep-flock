import os
from pygame import Color, Vector2

from src.animals.animals import Animal


def find_average_position_of_neighbors(neighbors):
    avg_position = Vector2(0, 0)
    for neighbor in neighbors:
        avg_position += neighbor.position
    avg_position /= len(neighbors)
    return avg_position


class Sheep(Animal):
    def __init__(self,id, position, velocity):
        super().__init__(id, position, velocity, Color(0,255,0,255))
        self.max_speed = float(os.getenv('SHEEP_MAX_SPEED'))

    def move(self, sheep: list, dogs: list):
        neighbors = self.find_neighbors(sheep, dogs)

        if not neighbors:
            return Vector2(0, 0)


        avg_position = find_average_position_of_neighbors(neighbors)

        # Calculate the steering vector towards the average position
        steering = avg_position - self.position
        self.velocity = steering
        self._limit_speed()

        self.position += self.velocity

    def _limit_speed(self):
        """
        Ensure the sheep's velocity does not exceed the maximum speed.
        """
        speed = self.velocity.magnitude()
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed