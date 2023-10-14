from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import Color  # for text
import random


# create a helper method for loading sprites.
def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)
    # load() returns a surface, which is an object used by Pygame to represent images

    # convert the image to a format that better fits the screen to speed up the drawing process
    if with_alpha:
        return loaded_sprite.convert_alpha()  # enables transparency
    else:
        return loaded_sprite.convert()  # no transparency


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

# Wrapping Objects Around the Screen
def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


# create a helper method for loading sounds, similar to the one for sprites.
def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)


# Create a font, create a surface, blit the surface onto the screen
def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)  # True for antialiasing

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)