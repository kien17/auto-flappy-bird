import pygame

class Bird:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.width = 30
        self.height = 30
        self.color = (255, 0, 0)
        self.velocity = 0
        self.gravity = 0.1
        self.icon_flap = pygame.image.load("Mimi_fly.png")
        self.icon_flap = pygame.transform.scale(self.icon_flap, (self.width, self.height))
        self.icon_fall = pygame.image.load("Mimi_roi.png")
        self.icon_fall = pygame.transform.scale(self.icon_fall, (self.width, self.height))
        self.icon = self.icon_fall
        self.time_since_flap = 0

    def draw(self, screen):
        screen.blit(self.icon, (self.x, self.y))
        if self.time_since_flap > 0:
            self.time_since_flap -= 1
        else:
            self.icon = self.icon_fall

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
        elif self.y > 570:
            self.y = 570

    def flap(self):
        self.icon = self.icon_flap
        self.time_since_flap = 10
        self.velocity = -3