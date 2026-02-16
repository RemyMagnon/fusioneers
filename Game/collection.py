from Atom import *
from FusionCards import atoms_discovered

badges_rects = [None] * 30


def show_collection(screen):
    background = pygame.draw.rect(screen, (0, 0, 0),
                                  (WIDTH - 400, 0, 400, HEIGHT))

    title_font = pygame.font.SysFont('Verdana', 40, bold=True)
    font = pygame.font.SysFont('Arial', 18)
    neon_font = pygame.font.SysFont('Papyrus', 50, bold=True)
    title_surf = title_font.render("Collection", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(WIDTH - 200, 50))
    start_pos = (title_rect.left, title_rect.bottom - 2)
    end_pos = (title_rect.right, title_rect.bottom - 2)
    pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 3)
    screen.blit(title_surf, title_rect)

    for atom in atoms_name:
        if atom == "Up quark" or atom == "Down quark":
            continue

        i = atoms_name.index(atom)

        if atom == "Neon-20":
            badge_name = neon_font.render(atom, True, (255, 95, 31))
            text_rect = badge_name.get_rect(center=(WIDTH - 230, 170 + 20 * i))
            screen.blit(badge_name, text_rect)
            dark_check_img = pygame.image.load(
                'Dark_check.png').convert_alpha()
            dark_check_img = pygame.transform.scale(dark_check_img, (90, 90))
            screen.blit(dark_check_img, (WIDTH - 100, 130 + 20 * i))
            if atoms_discovered[i]:
                check_img = pygame.image.load('checkmark.png').convert_alpha()
                check_img = pygame.transform.scale(check_img, (90, 90))
                screen.blit(check_img, (WIDTH - 100, 130 + 20 * i))
                badges_rects[i] = text_rect

            continue

        if i % 2 == 0:
            badge_name = font.render(atom, True, (255, 255, 255))
            text_rect = badge_name.get_rect(center=(WIDTH - 300, 100 + 20 * i))
            screen.blit(badge_name, text_rect)
            dark_check_img = pygame.image.load(
                'Dark_check.png').convert_alpha()
            dark_check_img = pygame.transform.scale(dark_check_img, (30, 30))
            screen.blit(dark_check_img, (WIDTH - 250, 85 + 20 * i))
            if atoms_discovered[i]:
                check_img = pygame.image.load('checkmark.png').convert_alpha()
                check_img = pygame.transform.scale(check_img, (30, 30))
                screen.blit(check_img, (WIDTH - 250, 85 + 20 * i))
                badges_rects[i] = text_rect

        else:
            badge_name = font.render(atom, True, (255, 255, 255))
            text_rect = badge_name.get_rect(
                center=(WIDTH - 100, 100 + 20 * (i - 1)))
            screen.blit(badge_name, text_rect)
            dark_check_img = pygame.image.load(
                'Dark_check.png').convert_alpha()
            dark_check_img = pygame.transform.scale(dark_check_img, (30, 30))
            screen.blit(dark_check_img, (WIDTH - 50, 85 + 20 * (i - 1)))
            if atoms_discovered[i]:
                check_img = pygame.image.load('checkmark.png').convert_alpha()
                check_img = pygame.transform.scale(check_img, (30, 30))
                screen.blit(check_img, (WIDTH - 50, 85 + 20 * (i - 1)))
                badges_rects[i] = text_rect

    return True
