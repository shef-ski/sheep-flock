import os
from pygame import Color, Vector2

from src.animals.animals import Animal
import random as rand


def find_average_position_of_neighbors(neighbors):
    avg_position = Vector2(0, 0)
    for neighbor in neighbors:
        avg_position += neighbor.position
    avg_position /= len(neighbors)
    return avg_position


class Dog(Animal):

    color = Color(tuple(map(int, os.getenv('COLOR_DOG').split(','))))

    def __init__(self, id, position, velocity):
        super().__init__(id, position, velocity, self.color)
        self.id = id
        self.max_speed = float(os.getenv('DOG_MAX_SPEED'))
        self.collision_radius = float(os.getenv('SHEEP_COLLISION_RADIUS'))
        self.d0 = float(os.getenv('D0_WEIGHT'))
        self.d1 = float(os.getenv('D1_COLLISION_WEIGHT'))
        self.d2 = float(os.getenv('D2_DOG_AVOIDANCE_WEIGHT'))
        self.d3 = float(os.getenv('D3_HUNT_WEIGHT'))
        self.d3_2 = float(os.getenv('D3_2_HUNT_PERP_WEIGHT'))
        self.d4 = float(os.getenv('D4_HUNT_stray_WEIGHT'))
        self.damping_factor = float(os.getenv('SHEEP_DAMPING_FACTOR'))
        self.l4 = float(os.getenv('DOG_AVOIDANCE_VELOCITY_WEIGHT'))
        self.dog_avoidance_radius = float(os.getenv('SHEEP_DOG_RECOGNITION_RADIUS'))

    def move(self, sheep: list, dogs: list):

        neighbors = self.find_neighbors_dog(sheep, dogs)

        if not neighbors:
            return Vector2(0, 0)

        # third formula (Separation)
        w1 = self._calculate_separation_velocity(sheep)

        # w4 dog avoidance
        w2 = self._calculate_dog_avoidance(dogs)

        w3 = self._catch_sheep(sheep)

        w4 = self._catch_stray(sheep)
        #print(w4.magnitude())

        if w4.magnitude() > 0.01 and self.id == 1:
            v_raw = (self.d4 * w4)
        else:
            v_raw = ((self.d0 * self.velocity)
                     + (self.d1 * w1)
                     + (self.d2 * w2)
                     + (self.d3 * w3)
                     + (self.d3_2 * w3.rotate(90)))



        self.velocity = self._limit_speed(v_raw, self.damping_factor)
        self.position += self.velocity

    def _limit_speed(self, v_raw, min_scalar, max_modifier=1):
        """
        Ensure the sheep's velocity does not exceed the maximum speed.
        """
        v_raw_magnitude = abs(v_raw.magnitude())
        epsilon = 1e-5

        return min((self.max_speed * max_modifier / (v_raw_magnitude + epsilon)), min_scalar) * v_raw

    def _calculate_separation_velocity(self, sheep):

        close_neighbors = [
            other for other in sheep
            if other != self and (self.position - other.position).magnitude() <= self.collision_radius
        ]

        if not close_neighbors:
            return Vector2(0, 0)  # No neighbors in collision radius

        # Calculate the average distance vector to close neighbors
        avg_distance_vector = Vector2(0, 0)
        for neighbor in close_neighbors:
            avg_distance_vector += (neighbor.position - self.position)
        avg_distance_vector /= len(close_neighbors)

        # The contribution to steer away from close neighbors
        return -avg_distance_vector

    def _calculate_dog_avoidance(self, dogs):
        close_dogs = [
            dog for dog in dogs
            if (self.position - dog.position).magnitude() <= self.dog_avoidance_radius
        ]

        if not close_dogs:
            return Vector2(0, 0)  # No dogs in avoidance radius

        avg_distance_vector = Vector2(0, 0)
        for dog in close_dogs:
            avg_distance_vector += (dog.position - self.position)
        avg_distance_vector /= len(close_dogs)

        return -avg_distance_vector

    def _catch_sheep(self, sheep):

        close_neighbors = [
            other for other in sheep
            if other != self and (self.position - other.position).magnitude() <= self.dog_observation_radius
        ]

        if not close_neighbors:
            return Vector2(0, 0)  # No neighbors in collision radius

        # Calculate the average distance vector to close neighbors
        avg_distance_vector = Vector2(0, 0)
        for neighbor in close_neighbors:
            avg_distance_vector += (neighbor.position - self.position)
        avg_distance_vector /= len(close_neighbors)

        # The contribution to steer away from close neighbors
        return avg_distance_vector

    def _catch_stray(self, sheep):

        close_neighbors = [
            other for other in sheep
            if other != self and (self.position - other.position).magnitude() <= self.dog_observation_radius
        ]

        if not close_neighbors:
            return Vector2(0, 0)  # No neighbors in collision radius

        # Calculate the average distance vector to close neighbors
        max_distance = 0
        push_pos = Vector2(0.0)
        tot_dis = 0
        for neighbor in close_neighbors:
            avg_pos = find_average_position_of_neighbors(close_neighbors)
            if (neighbor.position - avg_pos).magnitude() > max_distance:
                max_distance = (neighbor.position - avg_pos).magnitude()
                tot_dis += (neighbor.position - avg_pos).magnitude()
                # stray_sheep_pos = neighbor.position
                push_pos = neighbor.position + 0.1 * (neighbor.position - avg_pos)

        # The contribution to steer away from close neighbors
        if max_distance > (10 * tot_dis/len(close_neighbors) + 0.2):
            return push_pos - self.position
        else:
            return Vector2(0, 0)

