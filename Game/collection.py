from Atom import *
from FusionCards import atoms_discovered

badges_rects = [None] * 30


def show_collection(screen):
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 400, 0, 400, HEIGHT))

    title_font = pygame.font.SysFont('Verdana', 40, bold=True)
    font = pygame.font.SysFont('Arial', 18)
    neon_font = pygame.font.SysFont('Papyrus', 50, bold=True)
    title_surf = title_font.render("Collection", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(WIDTH - 200, 35))
    start_pos = (title_rect.left, title_rect.bottom - 2)
    end_pos = (title_rect.right, title_rect.bottom - 2)
    pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 3)
    screen.blit(title_surf, title_rect)

    for i, atom in enumerate(atoms_name):

        if atom == "Neon-20":
            font_used = neon_font
            color = (255, 95, 31)
            text_center = (WIDTH - 230, 150 + 20 * i)
            check_pos = (WIDTH - 100, 90 + 20 * i)
            check_size = (90, 90)
        else:
            font_used = font
            color = (255, 255, 255)

            if i % 2 == 0:
                text_center = (WIDTH - 300, 90 + 20 * i)
                check_pos = (WIDTH - 250, 75 + 20 * i)
            else:
                text_center = (WIDTH - 100, 90 + 20 * (i - 1))
                check_pos = (WIDTH - 50, 75 + 20 * (i - 1))

            check_size = (30, 30)

        # ---- Draw text ----
        badge_name = font_used.render(atom, True, color)
        text_rect = badge_name.get_rect(center=text_center)
        screen.blit(badge_name, text_rect)

        # ---- Choose check image ----
        if atoms_discovered[i]:
            img_path = 'checkmark.png'
            badges_rects[i] = text_rect
        else:
            img_path = 'Dark_check.png'
        check_img = pygame.image.load(img_path).convert_alpha()
        check_img = pygame.transform.scale(check_img, check_size)
        screen.blit(check_img, check_pos)