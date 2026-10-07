import pygame


class Bird:
    def __init__(self, x, y, radius=15, gravity=0.5, flap_strength=-8):
        self.x = x
        self.y = y
        self.radius = radius
        self.gravity = gravity
        self.flap_strength = flap_strength
        self.velocity = 0

    def flap(self):
        self.velocity = self.flap_strength

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def center(self):
        return (self.x, self.y)

    def rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )
