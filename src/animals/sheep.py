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
    def __init__(self, id, position, velocity):
        super().__init__(id, position, velocity, Color(0, 255, 0, 255))
        self.max_speed = float(os.getenv('SHEEP_MAX_SPEED'))
        self.collision_radius = float(os.getenv('SHEEP_COLLISION_RADIUS'))
        self.l0 = float(os.getenv('L0_WEIGHT'))
        self.l1 = float(os.getenv('L1_POSITION_WEIGHT'))
        self.l2 = float(os.getenv('L2_VELOCITY_WEIGHT'))
        self.l3 = float(os.getenv('L3_COLLISION_WEIGHT'))

    def move(self, sheep: list, dogs: list):

        neighbors = self.find_neighbors(sheep, dogs)

        if not neighbors:
            return Vector2(0, 0)
        # first formula
        w1 = self._calculate_alignment_velocity(neighbors)

        # second formula
        w2 = self._calculate_cohesion_velocity(neighbors)

        # third formula
        w3 = self._calculate_avoidance_velocity(sheep)

        v_raw = (self.velocity * self.l0) + (self.l1 * w1) + (self.l2 * w2) + (self.l3 * w3)
        self.velocity = self._limit_speed(v_raw)
        self.position += self.velocity

    def _limit_speed(self, v_raw):
        """
        Ensure the sheep's velocity does not exceed the maximum speed.
        """
        v_raw_magnitude = abs(v_raw.magnitude())
        return min((self.max_speed / v_raw_magnitude), 1) * v_raw

    def _calculate_alignment_velocity(self, neighbors):
        """
        Rule 1: Steer towards the average position of nearby boids.
        """
        avg_position = Vector2(0, 0)
        for neighbor in neighbors:
            avg_position += neighbor.position
        avg_position /= len(neighbors)

        steering = avg_position - self.position
        return steering

    def _calculate_cohesion_velocity(self, neighbors):
        """
        Rule 2: Align with the average velocity of nearby boids.
        """
        # Calculate the average velocity of neighbors
        avg_velocity = Vector2(0, 0)
        for neighbor in neighbors:
            avg_velocity += neighbor.velocity
        avg_velocity /= len(neighbors)

        # The contribution to align with neighbors' average velocity
        return avg_velocity

    def _calculate_avoidance_velocity(self, sheep):
        """
        Rule 3: Avoid neighbors that are too close (within collision radius).
        """
        close_neighbors = [
            other for other in sheep
            if other != self and (self.position - other.position).magnitude() <= self.collision_radius
        ]

        if not close_neighbors:
            return Vector2(0, 0)  # No neighbors in collision radius

        # Calculate the average distance vector to close neighbors
        avg_distance_vector = Vector2(0, 0)
        for neighbor in close_neighbors:
            avg_distance_vector += (self.position - neighbor.position)
        avg_distance_vector /= len(close_neighbors)

        # The contribution to steer away from close neighbors
        return -avg_distance_vector
