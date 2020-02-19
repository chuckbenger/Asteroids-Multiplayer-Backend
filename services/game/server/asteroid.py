import random
from typing import List


class Asteroid:
    def __init__(self, id, x, y, angle, sides, size, velocity,
                 rotation_speed, lives):
        self.id = id
        self.x = x
        self.y = y
        self.angle = angle
        self.sides = sides
        self.size = size
        self.velocity = velocity
        self.rotiation_speed = rotation_speed
        self.lives = lives

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "sides": self.sides,
            "size": self.size,
            "velocity": self.velocity,
            "rotation_speed": self.rotiation_speed,
            "lives": self.lives
        }


def generate_asteroid_field(size: int) -> List[Asteroid]:
    asteroids = []
    for i in range(size):
        asteroid = Asteroid(
            id=i,
            x=random.randint(0, 400),
            y=random.randint(0, 500),
            angle=random.randint(0, 360),
            sides=6,
            size=random.randint(20, 40),
            velocity=random.random(),
            rotation_speed=random.randint(1, 3),
            lives=2
        )
        asteroids.append(asteroid)
    return asteroids
