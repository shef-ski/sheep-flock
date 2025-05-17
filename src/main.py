import pygame
import sys
from dotenv import load_dotenv
load_dotenv()

from src.environment import Environment
import os
import random as rand
import numpy as np

seed = 2
rand.seed(seed)
np.random.seed(seed)

if __name__ == "__main__":
    n_sheep = int(os.getenv("N_SHEEP", 0))
    n_dogs = int(os.getenv("N_DOG", 0))
    env = Environment((800, 600), n_sheep, n_dogs)
    pygame.event.set_allowed([pygame.QUIT])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        env.draw()

