# Asteroids game code from realpython.com

# The general structure of a Pygame program is:
# initialize_pygame()
# while True:
#     handle_input()
#     process_game_logic()
#     draw_game_elements()
# The current state of the keyboard can be obtained using pygame.key.get_pressed()
# It returns a dictionary where key constants (like pygame.K_ESCAPE that you used
# previously) are keys, and the value is True if the key is pressed or False otherwise.

import pygame
from models import Spaceship, Asteroid
from utils import load_sprite, get_random_position, load_sound, print_text


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    def __init__(self):
        self._init_pygame()
        # create a display surface. Images in Pygame are represented by surfaces.
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()  # to control frame rate
        self.font = pygame.font.Font(None, 64)  # default font, 64 px high
        self.message = ""
        self.die_sound = load_sound("0017_explo_grenade_06_PremiumBeat")
        self.win_sound = load_sound("495005__evretro__win-video-game-sound louder")
        self.hit_sound = load_sound(("155235__zangrutz__bomb-small explosion freesound"))
        self.thrust_sound = load_sound(("395883__jokallset__flame-in-furnace 2sec"))
        self.thrusting = False
        self.win_sound_played = False  # flag to track if the win sound has been played

        self.bullets = []
        self.asteroids = []
        self.spaceship = Spaceship((400,300), self.bullets.append)

        for _ in range(6):  # create 6 big asteroids, not too close to spaceship
            while True:
                position = get_random_position(self.screen)
                if (position.distance_to(self.spaceship.position)
                > self.MIN_ASTEROID_DISTANCE):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        while True:
            # input, logic, graphics
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()  # a one-time initialization of Pygame
        pygame.display.set_caption("Space Rocks")  # display game name

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()  # enables the window "X" close button
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()  # enables Esc to close window
            elif self.spaceship and event.type == pygame.KEYDOWN \
                and event.key == pygame.K_SPACE:
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                if not self.thrusting:
                    self.thrusting = True
                    self.thrust_sound.play(-1)  # Start playing the thrust sound in a loop
                self.spaceship.accelerate()
            else:
                if self.thrusting:
                    self.thrusting = False
                    self.thrust_sound.stop()  # Stop the thrust sound

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        # Remove spaceship if asteroid hits it
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.die_sound.play()
                    self.message = "You lost!"
                    break

        # Remove asteroid if bullet hits it
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    self.hit_sound.play()
                    break

        # Surfaces in Pygame have a get_rect() method that returns a rectangle representing their area.
        # That rectangle, in turn, has a collidepoint() method that returns True
        # if a point is included in the rectangle and False otherwise.
        # Using these two methods, we can check if the bullet has left the screen,
        # and if so, remove it from the list.
        for bullet in self.bullets[:]:  # copies the list to allow element removal without errors
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        # If all asteroids destroyed, msg & music
        if not self.asteroids and self.spaceship:
            self.message = "You won!"
            if not self.win_sound_played:
                self.win_sound.play()
                self.win_sound_played = True  # Set the flag to True to indicate that the sound has been played

    # Helper method in the SpaceRocks class that returns all objects
    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects


    def _draw(self):
        self.screen.blit(self.background, (0,0))  # 0,0 = dist from top left cnr

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()  # updates the display for every frame
        self.clock.tick(60)  # arg specifies frames per sec

# Pygame offers a pygame.time.Clock class with a tick() method. This method will
# wait long enough to match the desired FPS value, passed as an argument.
