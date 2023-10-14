# Pygame also offers another class, Sprite, that’s intended as a base class for visible objects
from pygame.math import Vector2
# Vector2 has x & y coordinates. These can give position, motion or acceleration in a given direction.
from pygame.transform import rotozoom  # for scaling and rotating images
from utils import load_sprite, wrap_position, get_random_velocity, load_sound


class GameObject:  # implement a custom class for game objects
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2  # this gives the collision zone
        self.velocity = Vector2(velocity)

    def draw(self, surface):  # will draw the object’s sprite onto the surface passed as an argument.
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):  # will update the position of the game object.
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):  # collision detection. Returns T/F
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
# note that game objects have a central position, but blit() requires a top-left
# corner. So, the blit position has to be calculated by moving the actual position
# of the object by a vector. This happens in draw().


UP = Vector2(0, -1)


class Spaceship(GameObject):  # spaceship class which inherits from GameObject
    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("440661_seansecret_classic-laser-pew higher_pitch quietest")
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("spaceship"), Vector2(0))
    MANEUVERABILITY = 3  # angle in degrees by which spaceship’s direction can rotate each frame
    ACCELERATION = 0.25
    BULLET_SPEED = 3

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)  # rotate_ip() method of the Vector2 class rotates by degrees

    # override the draw method
    def draw(self, surface):
        angle = self.direction.angle_to(UP)  # angle_to() method of the Vector2 class
        rotated_surface = rotozoom(self.sprite, angle, 1.0)  # rotates the sprite
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)  # render/put image on screen

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        # create a bullet instance at the spaceship's current location
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)  # bullet is added to all the bullets in the game
        self.laser_sound.play()


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)  # arg2 = angle

        super().__init__(position, sprite, get_random_velocity(1,3))

    def split(self):
        if self.size > 1:
            for _ in range(2):  # creates 2 smaller asteroids
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1)
                self.create_asteroid_callback(asteroid)


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    # Override move() in the Bullet class in the space_rocks/models.py file
    def move(self, surface):
        self.position = self.position + self.velocity
