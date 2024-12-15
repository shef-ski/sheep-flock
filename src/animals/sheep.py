import os
from pygame import Color, Vector2
from src.animals.animals import Animal
from src.utils import timed
import random as rand


@timed
def find_average_position_of_neighbors(neighbors):
    avg_position = Vector2(0, 0)
    for neighbor in neighbors:
        avg_position += neighbor.position
    avg_position /= len(neighbors)
    return avg_position


class Sheep(Animal):

    color_default = Color(tuple(map(int, os.getenv('COLOR_SHEEP_DEFAULT').split(','))))
    color_excited = Color(tuple(map(int, os.getenv('COLOR_SHEEP_EXCITED').split(','))))

    def __init__(self, id, position, velocity):
        super().__init__(id, position, velocity, self.color_default)
        self.max_speed = float(os.getenv('SHEEP_MAX_SPEED'))
        self.collision_radius = float(os.getenv('SHEEP_COLLISION_RADIUS'))
        self.l0 = float(os.getenv('L0_WEIGHT'))
        self.l1 = float(os.getenv('L1_POSITION_WEIGHT'))
        self.l2 = float(os.getenv('L2_VELOCITY_WEIGHT'))
        self.l3 = float(os.getenv('L3_COLLISION_WEIGHT'))
        self.damping_factor = float(os.getenv('SHEEP_DAMPING_FACTOR'))
        self.l4 = float(os.getenv('DOG_AVOIDANCE_VELOCITY_WEIGHT'))
        self.dog_avoidance_radius = float(os.getenv('SHEEP_DOG_RECOGNITION_RADIUS'))

        self.excitement_duration = 0
        self.excitement_direction = None

    @property
    def is_excited(self):
        return self.excitement_duration > 0

    def excite(self, duration: int = 400):
        self.excitement_duration = duration
        self.color = self.color_excited

        random_dir = Vector2(
            rand.uniform(-1.5, 1.5),
            rand.uniform(-1.5, 1.5)
        )
        self.excitement_direction = random_dir

    def _update_excitingness(self):
        self.excitement_duration -= 1
        if self.excitement_duration == 0:
            self.color = self.color_default

        random_noise = Vector2(
            rand.uniform(-0.2, 0.2),
            rand.uniform(-0.2, 0.2)
        )
        self.excitement_direction += random_noise

    def move(self, sheep: list, dogs: list):
        if self.is_excited:
            self._update_excitingness()

        neighbors = self.find_neighbors(sheep, dogs)

        if not neighbors:
            return Vector2(0, 0)

        # first formula (Cohesion)
        w1 = self._calculate_cohesion_velocity(neighbors)

        # second formula (Alignment)
        w2 = self._calculate_alignment_velocity(neighbors)

        # third formula (Separation)
        w3 = self._calculate_separation_velocity(sheep)

        # w4 dog avoidance
        w4 = self._caluclate_dog_avoidance(dogs)

        if not self.is_excited:  # standard case
            v_raw = ((self.l0 * self.velocity)
                     + (self.l1 * w1)
                     + (self.l2 * w2)
                     + (self.l3 * w3)
                     + (self.l4 * w4))

            self.velocity = self._limit_speed(v_raw, self.damping_factor)

        else:
            movement = self.excitement_direction + (self.l4 * w4)
            self.velocity = self._limit_speed(movement, 1, 2)

        self.position += self.velocity

    @timed
    def _limit_speed(self, v_raw, min_scalar, max_modifier=1):
        """
        Ensure the sheep's velocity does not exceed the maximum speed.
        """
        v_raw_magnitude = abs(v_raw.magnitude())

        return min((self.max_speed * max_modifier / v_raw_magnitude), min_scalar) * v_raw

    @timed
    def _calculate_cohesion_velocity(self, neighbors):
        """
        Rule 1: Steer towards the average position of nearby boids.
        """
        avg_position = Vector2(0, 0)
        for neighbor in neighbors:
            avg_position += neighbor.position
        avg_position /= len(neighbors)

        steering = avg_position - self.position
        return steering

    @timed
    def _calculate_alignment_velocity(self, neighbors):
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

    @timed
    def _calculate_separation_velocity(self, sheep):
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
            avg_distance_vector += (neighbor.position - self.position)
        avg_distance_vector /= len(close_neighbors)

        # The contribution to steer away from close neighbors
        return -avg_distance_vector

    @timed
    def _caluclate_dog_avoidance(self, dogs):
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
