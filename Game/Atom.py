# Updated Nucleon subclass
import random
import pygame
import math
from Constants import *
import radioactivedecay as rd
import numpy as np

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
        "Ne-20"]


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
        "Neon-20"]


atoms_size = [
    2.5,
    2.5,
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
    15.0]


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
    (179, 227, 245)]


atoms_label = [
    "u",
    "d",
    "n",
    "¹H",
    "²H",
    "³H",
    "³He",
    "⁴He",
    "⁶Li",
    "⁷Li",
    "⁷Be",
    "¹⁰B",
    "¹⁰Be",
    "¹¹B",
    "¹⁰C",
    "¹¹C",
    "¹³N",
    "¹⁴O",
    "¹²C",
    "¹³C",
    "¹⁴C",
    "¹⁴N",
    "¹⁵N",
    "¹⁶O",
    "¹⁵O",
    "¹⁷O",
    "¹⁸O",
    "¹⁹F",
    "¹⁸F",
    "²⁰Ne"
]



class Atom():
    def __init__(self, name, x=random.uniform(0, WIDTH), y=random.uniform(0, HEIGHT)):
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.name = name
        if name not in atoms_symbols:
            raise TypeError("Not a valid atom! Check Atom.py for a full list.")
        elif name == "u":
            self.type = "quark"
            self.identity = "up quark"
            self.id = 2*10**6/3 + 10**3/3
            self.proton_number = 0
            self.neutron_number = 0
            self.half_life = float("inf")
            self.decays_into = []
            self.decay_type = []
            self.info = "Placeholder text."
            self.index = atoms_symbols.index(name)
        elif name == "d":
            self.type = "quark"
            self.identity = "down quark"
            self.id = -10**6/3 + 10**3/3
            self.proton_number = 0
            self.neutron_number = 0
            self.half_life = float("inf")
            self.decays_into = []
            self.decay_type = []
            self.info = "Placeholder text."
            self.index = atoms_symbols.index(name)
        elif name == "n":
            self.type = "neutron"
            self.identity = "neutron"
            self.id = 10000
            self.proton_number = 0
            self.neutron_number = 0
            self.half_life = 20
            self.decays_into = ["H-1"]
            self.decay_type = []
            self.info = "Placeholder text."
            self.index = atoms_symbols.index(name)
        else:
            self.type = "atom"
            self.identity = rd.Nuclide(name)
            self.id = self.identity.id
            self.proton_number = self.identity.Z
            self.neutron_number = self.identity.A - self.identity.Z
            self.decays_into = self.identity.progeny()
            self.decay_type = self.identity.decay_modes()
            self.info = "Placeholder text."
            self.index = atoms_symbols.index(name)
            self.half_life = np.log(self.identity.half_life())

        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.radius = atoms_size[self.index] * 3
        self.destroy = False

    def decay(self):
        if len(self.decays_into) > 0:
            import Game
            Game.add_atom(self.decays_into[0], self.x, self.y)
            Game.remove_atom(self)

    def update(self):
        self.apply_gravity(strength_multiplier=0.85)
        current_speed = math.hypot(self.vx, self.vy)
        if current_speed > optimal_speed_quarks:
            scale_factor = optimal_speed_quarks / current_speed
            self.vx *= scale_factor
            self.vy *= scale_factor

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
                overlap = dist + self.radius - (
                            BORDER_RADIUS - BORDER_THICKNESS)

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

        self.half_life -= 1/60

        if self.half_life <= 0:
            self.decay()

        if self.type == "atom" and self.half_life < float("inf"):
            pass
            # print(self.half_life)

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

    def draw(self, surface):
        import Game
        if self.half_life == float('inf') or Game.collection == True:
            x_offset = 0
            y_offset = 0
        else:
            x_offset = random.randint(-10, 10) * (np.exp(-self.half_life)+0.1)
            y_offset = random.randint(-10, 10) * (np.exp(-self.half_life)+0.1)
        sx, sy = Game.world_to_screen((self.x, self.y))
        radius = max(1, int(atoms_size[self.index] * 3 * Game.camera_zoom))
        pygame.draw.circle(surface, atoms_color[self.index], (int(sx+x_offset), int(sy+y_offset)), radius)
        if atoms_color[self.index][0] + atoms_color[self.index][1] + atoms_color[self.index][2] < 400:
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)

        font_size = max(8, int(20 * Game.camera_zoom))
        dynamic_font = pygame.font.SysFont(None, font_size)

        text = dynamic_font.render(atoms_symbols[self.index], True, color)
        rect = text.get_rect(center=(sx+x_offset, sy+y_offset))
        surface.blit(text, rect)
    
    def _generate_label(self):

        return atoms_label[self.index]

        """Generate a label with superscript notation for the atom."""
        superscript_map = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
        }
    
        if self.type == "neutron":
            return "n"
        
        if self.type == "atom":
            if self.name == "H-1":
                return "P"
            # Extract element symbol and mass number from name (e.g., "H-1" -> "H", "1")
            parts = self.name.split('-')
            if len(parts) == 2:
                element = parts[0]
                mass_num = parts[1]
                # Convert mass number to superscript
                superscript_mass = ''.join(superscript_map.get(digit, digit) for digit in mass_num)
                return f"{superscript_mass}{element}"
        
        return self.name


    @staticmethod
    def merge(a1, a2):
        if not isinstance(a2, Atom):
            return None
        if (a2.type == "atom" or a2.type == "neutron") and (a1.type == "atom" or a1.type == "neutron"):
            try:
                sum = str(rd.Nuclide(a1.id + a2.id))
            except ValueError:
                return None
            str_start = sum.index("Nuclide: ")
            str_end = sum.index(", decay")
            return sum[str_start + 9:str_end]
        else:
            print("Not an atom or neutron!")
            return None

    @staticmethod 
    def protonmerge(atom, proton):
        if not isinstance(proton, Atom):
            return None
        elif (atom.type == "atom" and proton.type == "proton") or (atom.type == "proton" and proton.type == "atom"):
            ID = atom.id + proton.id
            sum = str(rd.Nuclide(ID))
            str_start = sum.index("Nuclide: ")
            str_end = sum.index(", decay")
            sum = sum[str_start + 9:str_end]
            return sum
        else: 
            return None
    
    def quarkmerge(self, other1, other2):
        if not isinstance(other1, Atom) or not isinstance(other2, Atom):
            return None
        elif self.type and other1.type and other2.type == "quark":
            ID = self.id + other1.id + other2.id
            if ID == 10010000 or 10000000:
                sum = str(rd.Nuclide(ID))
                str_start = sum.index("Nuclide: ")
                str_end = sum.index(", decay")
                sum = sum[str_start + 9:str_end]
                return Atom(sum)
            else: 
                return None
        else: 
            return None

   
    def __str__(self):
        return self.name  

