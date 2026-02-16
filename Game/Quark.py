# Updated Quark subclass
import random
import math
import pygame
from Constants import *
from Particle import Particle

class Quark(Particle):
    def __init__(self, flavor):
        super().__init__()
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 2)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.flavor = flavor

    def update(self):
        self.apply_gravity()
        current_speed = math.hypot(self.vx, self.vy)
        if current_speed > optimal_speed_quarks:
            scale_factor = optimal_speed_quarks / current_speed
            self.vx *= scale_factor
            self.vy *= scale_factor
        self.update_position()

    def speed(self):
        return math.hypot(self.vx, self.vy)

    def draw(self, surface):
        import Game
        color = (255, 50, 50) if self.flavor == "up" else (50, 50, 255)
        sx, sy = Game.world_to_screen((self.x, self.y))
        radius = max(1, int(self.radius * Game.camera_zoom))
        pygame.draw.circle(surface, color, (int(sx), int(sy)), radius)
        label = "u" if self.flavor == "up" else "d"

        font_size = max(8, int(20 * Game.camera_zoom))
        dynamic_font = pygame.font.SysFont(None, font_size)

        text = dynamic_font.render(label, True, (255, 255, 255))
        rect = text.get_rect(center=(sx, sy))
        surface.blit(text, rect)
