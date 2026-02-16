# Particle superclass
import random
import math
from Constants import *

class Particle:
    def __init__(self, x=random.uniform(0, WIDTH), y=random.uniform(0, HEIGHT), radius=8):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.radius = radius
        self.destroy = False

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce off circular world border centered on the camera
        try:
            import Game
           
            # World center (where the border is actually located)
            world_center_x = WIDTH / 2
            world_center_y = HEIGHT / 2
    
            # Distance from particle to world center
            dx = self.x - world_center_x
            dy = self.y - world_center_y
            dist = math.hypot(dx, dy)

            if dist == 0:
                return

            # If particle is outside the border (taking its radius into account), push it back
            if dist + self.radius > (BORDER_RADIUS - BORDER_THICKNESS):
                nx = dx / dist
                ny = dy / dist
                overlap = dist + self.radius - (BORDER_RADIUS - BORDER_THICKNESS)

                # Move particle just inside the border
                self.x -= nx * overlap
                self.y -= ny * overlap

                # Reflect velocity about the normal and apply a small damping
                v_dot_n = self.vx * nx + self.vy * ny
                if v_dot_n > 0:
                    self.vx -= 2 * v_dot_n * nx
                    self.vy -= 2 * v_dot_n * ny

                    # Add variation to the bounce
                    self.vx *= random.uniform(0.95, 1.1)
                    self.vy *= random.uniform(0.95, 1.1)
        except Exception:
            # If Game or camera not available, fall back to simple modulo wrap
            self.x %= WIDTH
            self.y %= HEIGHT

    def apply_gravity(self, strength_multiplier=QUARK_ATTRACTION_MULTIPLIER):
        import Game
        if Game.gravity_active:
            dx = Game.gravity_pos[0] - self.x
            dy = Game.gravity_pos[1] - self.y
            dist = math.hypot(dx, dy)
            if dist > 5:
                force = (GRAVITY_STRENGTH * strength_multiplier) * GRAVITY(dist)
                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force

