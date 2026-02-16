from Atom import *
from Constants import *

atom_full_data = [
    ["Stable", "N/A", 1964,
     "The lightest of all quarks; it makes protons stable."],
    ["Stable", "N/A", 1964,
     "Slightly heavier than the Up quark; it helps make neutrons."],
    ["Unstable", "611.0 s", 1932,
     "Made of two down quarks and one up quark, free neutrons decay in about 15 minutes."],
    ["Stable", "N/A", 1919,
     "Composed of a single proton, or two up quarks and one down quark. It is the most abundant atom in the universe."],
    ["Stable", "N/A", 1931,
     "Also called deuterium, this isotope is used in heavy water for nuclear fusion."],
    ["Unstable", "12.32 y", 1934,
     "This atom, also called tritium, is used to make watch hands glow. It is the smallest element that undergoes beta decay."],
    ["Stable", "N/A", 1939,
     "Much rarer than its counterpart He-4, it is theoretically a good source of fusion energy."],
    ["Stable", "N/A", 1895,
     "Also called an alpha particle, the nucleus of this common element is released during alpha decay."],
    ["Stable", "N/A", 1921,
     "Valuable for its use as a source material for producing H-3."],
    ["Stable", "N/A", 1921,
     f"The most abundant lithium isotope, it is used in lithium-ion batteries."],
    ["Unstable", "53.22 d", 1938,
     "The smallest element that decays via electron capture."],
    ["Stable", "N/A", 1920,
     "Also called enriched boron, this element is used to capture neutrons."],
    ["Unstable", "1.39 My", 1947,
     "A rare isotope found in ice cores that helps track solar activity."],
    ["Stable", "N/A", 1920,
     "It is transparent to neutrons and makes up 80% of natural boron."],
    ["Unstable", "19.3 s", 1949,
     "A very short-lived isotope that turns into Boron in just 19 seconds."],
    ["Unstable", "20.34 m", 1934,
     "Used in PET scans to visualize the human brain."],
    ["Unstable", "9.97 m", 1934,
     "Used in heart imaging to measure blood flow."],
    ["Unstable", "70.62 s", 1949,
     "A rare, short-lived oxygen that helps power stars in the CNO cycle."],
    ["Stable", "N/A", 1919,
     "The standard! One 'atomic mass unit' is defined as 1/12th of this atom."],
    ["Stable", "N/A", 1929,
     "Unlike C-12, this carbon is magnetic and used in chemical analysis (NMR)."],
    ["Unstable", "5700 y", 1940,
     "Radiocarbon! It is used to date ancient artifacts and fossils."],
    ["Stable", "N/A", 1919,
     "The main ingredient of Earth's atmosphere (about 99.6% of nitrogen)."],
    ["Stable", "N/A", 1930,
     "Stable and rare, it is used as a tracer in biology and to study proteins with NMR."],
    ["Stable", "N/A", 1919,
     "A 'double magic' nucleus, making it incredibly stable and abundant."],
    ["Unstable", "122.2 s", 1934,
     "Used in medical scans to measure oxygen use in the brain."],
    ["Stable", "N/A", 1929,
     "A rare, heavy oxygen used to study how plants use water."],
    ["Stable", "N/A", 1929,
     "Climate thermometer! Its ratio in ice tells us about ancient temperatures."],
    ["Stable", "N/A", 1920,
     "The only stable isotope of fluorine; essentially 100% of natural fluorine."],
    ["Unstable", "109.7 m", 1937,
     "The superstar of medical imaging; used to detect cancer in FDG-PET scans."],
    ["Stable", "N/A", 1913,
     "The first isotope ever discovered (in 1913); it glows red-orange in signs."]
]

atoms_discovered = [False] * 30


class Popup:
    def __init__(self, x, y, width, height, title, text, stability, halflife,
                 year, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)  # Light Gray
        self.title = title
        self.text = text
        self.is_visible = False
        self.line_spacing = 30
        self.padding = 15
        self.color = color
        self.body_color = (30, 30, 45)
        self.header_height = 40
        self.exit_button = pygame.Rect(self.rect.x + self.header_height / 4,
                                       self.rect.y + self.header_height / 4,
                                       20, 20)

        self.title_font = pygame.font.SysFont(TITLE_FONT, TITLE_FONT_SIZE,
                                              bold=True)
        self.font = pygame.font.SysFont(TEXT_FONT, TEXT_FONT_SIZE)

        self.stability = stability
        self.halflife = halflife
        self.year = year

    def get_wrapped_lines(self):
        words = self.text.split(' ')
        lines = []
        current_line = ""
        max_text_width = self.rect.width - (self.padding * 2)

        for word in words:
            # Check if adding the next word exceeds the width
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < max_text_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)  # Add the final line
        return lines

    def draw(self, screen):
        if self.is_visible:
            # Shadow effect
            shadow_offset = 7
            shadow_rect = self.rect.move(shadow_offset, shadow_offset)
            pygame.draw.rect(screen, self.color, shadow_rect, border_radius=15)
            pygame.draw.rect(screen, self.color, (self.rect.x + shadow_offset,
                                                  self.rect.y + shadow_offset,
                                                  self.rect.width,
                                                  self.header_height))

            # Main Box
            pygame.draw.rect(screen, self.body_color, self.rect,
                             border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2,
                             border_radius=15)  # Border

            # Render Wrapped Text
            lines = self.get_wrapped_lines()
            for i, line in enumerate(lines):
                line_surf = self.font.render(line.strip(), True,
                                             (255, 255, 255))
                # Position each line based on its index
                line_y = self.rect.y + self.header_height + self.padding + (
                        i * self.line_spacing)

                # Check to make sure we don't draw outside the box bottom
                if line_y < self.rect.bottom - self.padding:
                    screen.blit(line_surf,
                                (self.rect.x + self.padding, line_y))

            # ... (after your existing for loop that renders lines) ...

            # 1. Get the starting Y position for the extra data
            # We'll put it 2 lines below the last line of the main text
            current_data_y = line_y + (self.line_spacing * 2)

            extra_info = [
                f"Stability: {self.stability}",
                f"Half-life: {self.halflife}",
                f"Discovered: {self.year}"
            ]

            # 3. Draw the extra lines
            for j, info_text in enumerate(extra_info):
                # We use a slightly different color (e.g., light blue) to make it look like "data"
                info_surf = self.font.render(info_text, True, (180, 255, 255))
                info_y = current_data_y + (j * self.line_spacing)

                if info_y < self.rect.bottom - self.padding:
                    screen.blit(info_surf,
                                (self.rect.x + self.padding, info_y))

            # Title box

            header_rect = pygame.Rect(self.rect.x, self.rect.y,
                                      self.rect.width, self.header_height)
            pygame.draw.rect(screen, self.color, header_rect)
            pygame.draw.line(screen, (255, 255, 255),
                             (self.rect.x, self.rect.y + self.header_height),
                             (self.rect.right - 1,
                              self.rect.y + self.header_height), 2)

            # Title text
            title_surf = self.title_font.render(self.title, True, (0, 0, 0))
            title_rect = title_surf.get_rect(center=header_rect.center)
            screen.blit(title_surf, title_rect)

            # exit button
            pygame.draw.rect(screen, (0, 0, 0), self.exit_button)
            # Line 1: Top-left to bottom-right
            x_margin = 5
            pygame.draw.line(screen, (255, 255, 255),
                             (self.exit_button.x + x_margin,
                              self.exit_button.y + x_margin),
                             (self.exit_button.right - x_margin,
                              self.exit_button.bottom - x_margin), 3)
            # Line 2: Top-right to bottom-left
            pygame.draw.line(screen, (255, 255, 255),
                             (self.exit_button.right - x_margin,
                              self.exit_button.y + x_margin),
                             (self.exit_button.x + x_margin,
                              self.exit_button.bottom - x_margin), 3)

    def toggle(self):
        self.is_visible = not self.is_visible

    def handle_exit(self, event):
        if self.is_visible and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click only
                # Check if the click position is inside your exit_square
                if self.exit_button.collidepoint(event.pos):
                    self.is_visible = False


class Discoveries(Popup):
    def __init__(self, element, x=None, y=None):
        index = atoms_symbols.index(element)
        WIDTH = 400
        HEIGHT = 250
        if x == None and y == None:
            super().__init__((WIDTH * 2.4), (HEIGHT * 0.2), WIDTH, HEIGHT,
                             atoms_name[index], atom_full_data[index][3],
                             atom_full_data[index][0],
                             atom_full_data[index][1],
                             atom_full_data[index][2], atoms_color[index])
        else:
            super().__init__(x, y, WIDTH, HEIGHT,
                             atoms_name[index], atom_full_data[index][3],
                             atom_full_data[index][0],
                             atom_full_data[index][1],
                             atom_full_data[index][2], atoms_color[index])