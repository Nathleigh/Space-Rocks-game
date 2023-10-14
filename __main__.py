# Asteroids game code from realpython.com
# "Build an Asteroids Game With Python and Pygame", by Paweł Fertyk

from game import SpaceRocks
import os
os.chdir('..')


if __name__ == "__main__":
    space_rocks = SpaceRocks()  # start a game instance
    space_rocks.main_loop()  # input, logic, graphics
