import random
import math
from typing import List


class Asteroid:
    def __init__(self, id, x, y, angle, sides, size, velocity,
                 rotation_speed, lives, color):
        self.id = id
        self.x = x
        self.y = y
        self.angle = angle
        self.sides = sides
        self.size = size
        self.velocity = velocity
        self.rotiation_speed = rotation_speed
        self.lives = lives
        self.color = color

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "sides": self.sides,
            "size": self.size,
            "velocity": self.velocity,
            "rotationSpeed": self.rotiation_speed,
            "lives": self.lives,
            "color": self.color
        }


def random_color() -> str:
    letters = '0123456789ABCDEF'
    color = []
    color.append('#')

    for _ in range(6):
        letter = letters[random.randint(0, len(letters)-1)]
        color.append(letter)

    return ''.join(color)


def generate_asteroid_field(size: int) -> List[Asteroid]:
    asteroids = []

    _maxX = 1024
    _minX = 0
    _maxY = 1024
    _minY = 0

    leftRight = random.randint(1, 50)

    if leftRight <= 25:
        _maxX = (_maxX // 2) - (_maxX // 10)
    else:
        _minX = (_maxX // 2) + (_maxX // 10)

    topBottom = random.randint(1, 50)

    if topBottom <= 25:
        _maxY = (_maxY // 2) - (_maxY // 10)
    else:
        _minY = (_maxY // 2) + (_maxY // 10)

    for i in range(size):
        asteroid = Asteroid(
            id=i,
            x=random.randint(_minX, _maxX),
            y=random.randint(_minY, _maxY),
            angle=random.randint(0, 360) * (math.pi / 180),
            sides=6,
            size=random.randint(20, 80),
            velocity=random.uniform(.5, 2.0),
            rotation_speed=0,
            lives=1,
            color=random_color()
        )
        asteroids.append(asteroid)
    return asteroids
