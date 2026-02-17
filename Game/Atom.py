import random
import pygame
import math
from Constants import *
import radioactivedecay as rd
import FusionCards

atoms_symbols = [
        "u",
        "d",
        "n",
        "H-1",
        "H-2",
        "H-3",
        "He-3",
        "He-4",
        "Li-6",
        "Li-7",
        "Be-7",
        "B-10",
        "Be-10",
        "B-11",
        "C-10",
        "C-11",
        "N-13",
        "O-14",
        "C-12",
        "C-13",
        "C-14",
        "N-14",
        "N-15",
        "O-16",
        "O-15",
        "O-17",
        "O-18",
        "F-19",
        "F-18",
        "Ne-20"
]


atoms_label = [
        "u",
        "d",
        "n",
        "H1",
        "H 2",
        "H 3",
        "He 3",
        "He 4",
        "Li 6",
        "Li 7",
        "Be 7",
        "B 10",
        "Be 10",
        "B 11",
        "C 10",
        "C 11",
        "N 13",
        "O 14",
        "C 12",
        "C 13",
        "C 14",
        "N 14",
        "N 15",
        "O 16",
        "O 15",
        "O 17",
        "O 18",
        "F 19",
        "F 18",
        "Ne 20"
]


atoms_name = [
        "Up quark",
        "Down quark",
        "Neutron",
        "Hydrogen-1",
        "Hydrogen-2",
        "Hydrogen-3",
        "Helium-3",
        "Helium-4",
        "Lithium-6",
        "Lithium-7",
        "Beryllium-7",
        "Boron-10",
        "Beryllium-10",
        "Boron-11",
        "Carbon-10",
        "Carbon-11",
        "Nitrogen-13",
        "Oxygen-14",
        "Carbon-12",
        "Carbon-13",
        "Carbon-14",
        "Nitrogen-14",
        "Nitrogen-15",
        "Oxygen-16",
        "Oxygen-15",
        "Oxygen-17",
        "Oxygen-18",
        "Fluorine-19",
        "Fluorine-18",
        "Neon-20"
]


atoms_size = [
    1.5,
    1.5,
    5.0,
    5.0,
    10.7,
    8.8,
    9.85,
    8.4,
    12.95,
    12.2,
    13.25,
    12.25,
    11.8,
    12.05,
    12.5,
    12.4,
    12.65,
    13.0,
    12.35,
    12.3,
    12.5,
    12.7,
    12.75,
    13.5,
    13.05,
    13.45,
    13.65,
    14.5,
    14.0,
    15.0
]


atoms_color = [
    (255, 50, 50),
    (50, 50, 255),
    (128, 128, 128),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (217, 255, 255),
    (217, 255, 255),
    (204, 128, 255),
    (204, 128, 255),
    (194, 255, 0),
    (255, 181, 181),
    (194, 255, 0),
    (255, 181, 181),
    (144, 144, 144),
    (144, 144, 144),
    (48, 80, 248),
    (255, 13, 13),
    (144, 144, 144),
    (144, 144, 144),
    (144, 144, 144),
    (48, 80, 248),
    (48, 80, 248),
    (255, 13, 13),
    (255, 13, 13),
    (255, 13, 13),
    (255, 13, 13),
    (144, 224, 80),
    (144, 224, 80),
    (179, 227, 245)
]

atoms_text_color = []
for color in atoms_color:
    if sum(color) < 400:
        atoms_text_color.append((255, 255, 255))
    else:
        atoms_text_color.append((0, 0, 0))


class Atom:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.name = name
        self.index = atoms_symbols.index(name)
        self.radius = atoms_size[self.index] * 3
        if name == "u":
            self.id = 2*10**6/3 + 10**3/3
            self.half_life = float("inf")
            self.decays_into = []
        elif name == "d":
            self.id = -10**6/3 + 10**3/3
            self.half_life = float("inf")
            self.decays_into = []
        elif name == "n":
            self.id = 10000
            self.half_life = 20
            self.decays_into = ["H-1"]
        else:
            self.id = rd.Nuclide(name).id
            self.half_life = math.log(rd.Nuclide(name).half_life())
            self.decays_into = rd.Nuclide(name).progeny()


    def decay(self):
        if len(self.decays_into) > 0:
            import Game
            Game.add_atom(self.decays_into[0], self.x, self.y)
            Game.remove_atom(self)
            discovery = FusionCards.new_discovery(self.decays_into[0])
            if discovery is not None:
                Game.popup.append(discovery)


    def update(self):
        self.apply_gravity()
        current_speed = math.hypot(self.vx, self.vy)
        if current_speed > optimal_speed_quarks:
            scale_factor = optimal_speed_quarks / current_speed
            self.vx *= scale_factor
            self.vy *= scale_factor

        self.x += self.vx + random.uniform(-20, 20) * (math.exp(-self.half_life) + 0.05)
        self.y += self.vy + random.uniform(-20, 20) * (math.exp(-self.half_life) + 0.05)

        # Bounce off circular world border
        # Distance from particle to world center
        dx = self.x - WIDTH / 2
        dy = self.y - HEIGHT / 2
        dist = math.hypot(dx, dy)

        # If particle is outside the border (taking its radius into account), push it back
        if dist + self.radius > (BORDER_RADIUS - BORDER_THICKNESS):
            nx = dx / dist
            ny = dy / dist
            overlap = dist + self.radius - (BORDER_RADIUS - BORDER_THICKNESS)

            # Move particle just inside the border
            self.x -= nx * overlap
            self.y -= ny * overlap

            # Reflect velocity about the normal
            v_dot_n = self.vx * nx + self.vy * ny
            self.vx -= 2 * v_dot_n * nx
            self.vy -= 2 * v_dot_n * ny

        self.half_life -= 1/60

        if self.half_life <= 0:
            self.decay()


    def apply_gravity(self):
        import Game
        if Game.gravity_active:
            dx = Game.gravity_pos[0] - self.x
            dy = Game.gravity_pos[1] - self.y
            dist = math.hypot(dx, dy)
            if dist > 5:
                force = GRAVITY_STRENGTH * 2.72**(-dist / GRAVITY_RANGE) / dist
                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force


    def draw(self, surface):
        import Game
        sx, sy = Game.world_to_screen((self.x, self.y))
        radius = max(1, int(atoms_size[self.index] * 3 * Game.camera_zoom))
        pygame.draw.circle(surface, atoms_color[self.index], (sx, sy), radius)

        if Game.camera_zoom > 0.8 and not self.is_quark():
            text = Game.font.render(atoms_label[self.index], True, atoms_text_color[self.index])
            rect = text.get_rect(center=(sx, sy))
            surface.blit(text, rect)


    def merge(self, other):
        if self.is_quark and other.is_quark:
            try:
                str_sum = str(rd.Nuclide(self.id + other.id))
            except ValueError:
                return None
            str_start = str_sum.index("Nuclide: ")
            str_end = str_sum.index(", decay")
            return str_sum[str_start + 9:str_end]
        return None

   
    def __str__(self):
        return self.name

    def is_quark(self):
        return self.name == "u" or self.name == "d"