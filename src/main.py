import pygame
import sys

from dotenv import load_dotenv

from enviroment import Enviroment

load_dotenv()

def main():
    print("Hello world")

if __name__ == "__main__":
    env = Enviroment((800,800), 10, 50)
    paused = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        if not paused:
            env.draw()

