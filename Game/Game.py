import pygame
import random
import math

pygame.init()

import FusionCards
from Constants import *
from Atom import Atom, atoms_symbols
from collection import show_collection, badges_rects


pygame.mixer.init()
tone = pygame.mixer.Sound("100hz_tone.wav")
tone.set_volume(1.0)
channel = None  # We'll use a specific channel to control the sound

#Background music
pygame.mixer.music.load("Arron.mp3")
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Journey to the 10th Element")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)

particles = []
popup = []
cards = []
gravity_active = False
gravity_pos = (0, 0)

#music info
music_on = True

#camera information
camera_zoom = DEFAULT_ZOOM
camera_x = WIDTH/2
camera_y = HEIGHT/2
follow_mode = True


def clamp_camera():
    global camera_x, camera_y
    
    # The world center (where the character is)
    world_center_x = WIDTH / 2
    world_center_y = HEIGHT / 2
    
    # Maximum distance the camera can move from center
    # Scale with zoom - when zoomed in, allow more camera movement
    max_camera_offset = MAX_OFFSET / camera_zoom
    
    # Clamp camera position to stay within bounds of world center
    camera_x = max(world_center_x - max_camera_offset,  min(world_center_x + max_camera_offset, camera_x))
    camera_y = max(world_center_y - max_camera_offset,  min(world_center_y + max_camera_offset, camera_y))
    
def cursor_follow_camera(mouse_pos):
    global camera_x, camera_y
    
    # Get mouse position in screen coordinates
    mouse_x, mouse_y = mouse_pos
    
    # Calculate offset from screen center to mouse
    offset_x = mouse_x - (WIDTH / 2)
    offset_y = mouse_y - (HEIGHT / 2)
    
    # Limit the offset
    distance = math.hypot(offset_x, offset_y)
    if distance > MAX_OFFSET:
        offset_x = (offset_x / distance) * MAX_OFFSET
        offset_y = (offset_y / distance) * MAX_OFFSET
    
    # Apply distance multiplier to scale the effect
    offset_x *= DISTANCE_MULTIPLIER
    offset_y *= DISTANCE_MULTIPLIER
    
    # Target camera position (world center + offset)
    target_camera_x = (WIDTH / 2) + offset_x
    target_camera_y = (HEIGHT / 2) + offset_y
    
    # Smooth interpolation
    t = 1 - math.exp(-RESPONSIVENESS)
    camera_x += (target_camera_x - camera_x) * t
    camera_y += (target_camera_y - camera_y) * t
    
    # Apply bounds
    clamp_camera()


def world_to_screen(pos):
    wx, wy = pos
    sx = (wx - camera_x) * camera_zoom + WIDTH / 2
    sy = (wy - camera_y) * camera_zoom + HEIGHT / 2
    return sx, sy


def screen_to_world(pos):
    sx, sy = pos
    wx = (sx - WIDTH / 2) / camera_zoom + camera_x
    wy = (sy - HEIGHT / 2) / camera_zoom + camera_y
    return wx, wy


def zoom_at(screen_pos, zoom_factor):
    global camera_zoom, camera_x, camera_y
    if zoom_factor == 1.0:
        return
    before = screen_to_world(screen_pos)
    camera_zoom = max(ZOOM_MIN, min(ZOOM_MAX, camera_zoom * zoom_factor))
    camera_x = before[0] - (screen_pos[0] - WIDTH / 2) / camera_zoom
    camera_y = before[1] - (screen_pos[1] - HEIGHT / 2) / camera_zoom
    clamp_camera()

# ---------------- COLLISION ----------------

def resolve_collision(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    dist = math.hypot(dx, dy)

    if dist == 0:
        return

    overlap = a.radius + b.radius - dist
    if overlap > 0:
        nx = dx / dist
        ny = dy / dist

        a.x -= nx * overlap / 2
        a.y -= ny * overlap / 2
        b.x += nx * overlap / 2
        b.y += ny * overlap / 2

        dvx = a.vx - b.vx
        dvy = a.vy - b.vy
        impact_speed = dvx * nx + dvy * ny

        impulse = -impact_speed
        a.vx += impulse * nx
        a.vy += impulse * ny
        b.vx -= impulse * nx
        b.vy -= impulse * ny


def handle_collisions():
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            resolve_collision(particles[i], particles[j])


#    Apply subtle attraction to other clusters based on distance.
#    max_force: max acceleration applied per frame
#    min_distance: distance below which force is capped

def apply_cluster_attraction(nucleon, particles, max_force=-0.01, min_distance=20):
    my_cluster = [nucleon]
    my_center_x = sum(q.x for q in my_cluster) / len(my_cluster)
    my_center_y = sum(q.y for q in my_cluster) / len(my_cluster)

    for other in particles:
        if isinstance(other, Atom) and other.name == "H-1" and other not in my_cluster:
            other_cluster = [other]
            other_center_x = sum(q.x for q in other_cluster) / len(other_cluster)
            other_center_y = sum(q.y for q in other_cluster) / len(other_cluster)

            dx = other_center_x - my_center_x
            dy = other_center_y - my_center_y
            distance = math.hypot(dx, dy)

            if distance > 0:
                # Force magnitude inversely proportional to distance
                force = min(max_force, max_force * (min_distance / distance))
                # Direction normalized
                ax = (dx / distance) * force
                ay = (dy / distance) * force

                # Apply to entire cluster
                for q in my_cluster:
                    q.vx += ax
                    q.vy += ay
                # Optionally, pull the other cluster slightly back
                for q in other_cluster:
                    q.vx -= ax * 0.2
                    q.vy -= ay * 0.2


# ---------------- MERGING ----------------

"""
def check_merge():

    for i in range(len(particles)):
        cluster = [particles[i]]
        types = [particles[i].name]

        for j in range(len(particles)):

            dx = particles[i].x - particles[j].x
            dy = particles[i].y - particles[j].y
            if (((particles[i].is_quark and particles[j].is_quark) or (not particles[i].is_quark and not particles[j].is_quark))
                    and particles[i] != particles[j]
                    and math.hypot(dx, dy) <= particles[i].radius + particles[j].radius):
                cluster.append((particles[j]))
                types.append(particles[j].name)

            if len(cluster) == 3 and cluster[0].is_quark:
                if types.count("u") == 0 or types.count("d") == 0:
                    cluster.remove(particles[j])
                else:
                    avg_x = sum(quark.x for quark in cluster) / 3
                    avg_y = sum(quark.y for quark in cluster) / 3

                    if types.count("u") >= 2:
                        name = "H-1"
                    else:
                        name = "n"

                    add_atom(name, avg_x, avg_y)
                    Popup.new_discovery(name)

                    for quark in cluster:
                        remove_atom(quark)

                    # Spawn exactly three new quarks on merge
                    new_quarks = ["u", "d", random.choice(["u", "d"])]
                    for k in range(3):
                        distance = random.uniform(0, BORDER_RADIUS)
                        angle = random.uniform(0, 2 * math.pi)
                        new_x = distance * math.cos(angle)
                        new_y = distance * math.sin(angle)
                        add_atom(new_quarks[k], new_x, new_y)

                    break

            if len(cluster) == 2 and not cluster[0].is_quark:
                name = Atom.merge(cluster[0], cluster[1])

                if name in atoms_symbols:
                    avg_x = sum(atom.x for atom in cluster) / 2
                    avg_y = sum(atom.y for atom in cluster) / 2

                    add_atom(name, avg_x, avg_y)
                    Popup.new_discovery(name)

                    for quark in cluster:
                        remove_atom(quark)

                    break
"""



def check_atom_merging():
    atoms = [p for p in particles if (isinstance(p, Atom) and not p.is_quark())]

    for i in range(len(atoms)):
        cluster = []

        for j in range(len(atoms)):
            dx = atoms[i].x - atoms[j].x
            dy = atoms[i].y - atoms[j].y
            if math.hypot(dx, dy) <= atoms[i].radius + atoms[j].radius:
                cluster.append(atoms[j])
        
        if len(cluster) >= 2:
            group = cluster[:2]

            name = group[0].merge(group[1])
            
            if name is not None and name in atoms_symbols:

                avg_x = sum(q.x for q in group) / len(group)
                avg_y = sum(q.y for q in group) / len(group)

                #print("Merged atoms: " + group[0].name + " and " + group[1].name)
                #print("Merged :", name)

                add_atom(name, avg_x, avg_y)
                discovery = FusionCards.new_discovery(name)
                if discovery is not None:
                    popup.append(discovery)

                for q in group:
                    remove_atom(q)

                break



def check_quarks_merging():
    quarks = [p for p in particles if (p.name == "u" or p.name == "d")]

    for i in range(len(quarks)):
        cluster = []

        for j in range(len(quarks)):
            dx = quarks[i].x - quarks[j].x
            dy = quarks[i].y - quarks[j].y
            if math.hypot(dx, dy) < MERGE_DISTANCE:
                cluster.append(quarks[j])

        if len(cluster) >= 3:
            group = cluster[:3]

            if all(math.hypot(q.vx, q.vy) < MERGE_SPEED_THRESHOLD for q in group):

                flavors = [q.name for q in group]

                if flavors.count("u") == 2 and flavors.count("d") == 1:
                    name = "H-1"
                elif flavors.count("d") == 2 and flavors.count("u") == 1:
                    name = "n"
                else:
                    continue

                avg_x = sum(q.x for q in group) / 3
                avg_y = sum(q.y for q in group) / 3

                #print("Merged quarks: " + group[0].flavor + " and " + group[1].flavor)
                #print("Merged :", name)

                add_atom(name, avg_x, avg_y)
                discovery = FusionCards.new_discovery(name)
                if discovery is not None:
                    popup.append(discovery)

                for q in group:
                    remove_atom(q)

                # Spawn exactly three new quarks on merge
                for name in ["u", "d", random.choice(["u", "d"])]:
                    distance = random.uniform(0, BORDER_RADIUS)
                    angle = random.uniform(0, 2 * math.pi)
                    add_atom(name, WIDTH/2 + distance * math.cos(angle), HEIGHT/2 + distance * math.sin(angle))

                break



@staticmethod
def add_atom(name, x, y):
    if name in atoms_symbols:
        particles.append(Atom(name, x, y))

@staticmethod
def remove_atom(atom):
    particles.remove(atom)

# ---------------- INIT ----------------
for i in range(NUM_QUARKS):
    name = "u" if i % 2 == 0 else "d"
    distance = random.uniform(0, BORDER_RADIUS)
    angle = random.uniform(0, 2 * math.pi)
    add_atom(name, WIDTH/2 + distance * math.cos(angle), HEIGHT/2 + distance * math.sin(angle))


#------------- COLLECTION --------------
book_img = pygame.image.load('book.png').convert_alpha()
book_img = pygame.transform.scale(book_img, (60, 60))
collection = False

# ---------------- LOOP ----------------

running = True
while running:
    clock.tick(60)
    screen.fill((15, 15, 30))
    # Draw circular border centered on camera (screen center) and scaled by zoom
    
    center = world_to_screen((WIDTH/2, HEIGHT/2))
    radius = max(1, int(BORDER_RADIUS * camera_zoom))
    border_thickness = max(1, int(BORDER_THICKNESS * camera_zoom))
    
    outer_radius = max(1, int(OUTER_BORDER_RADIUS * camera_zoom))
    outer_border_thickness = max(1, int(OUTER_BORDER_THICKNESS * camera_zoom))
    pygame.draw.circle(screen, BORDER_COLOR, center, radius, border_thickness)
    pygame.draw.circle(screen, (5,5,7), center, outer_radius, outer_border_thickness)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for popups in popup:
            popups.handle_exit(event)

        for card in cards:
            card.handle_exit(event)

        # Gravity well controls
        if event.type == pygame.MOUSEBUTTONDOWN:
            gravity_active = True

        if event.type == pygame.MOUSEBUTTONUP:
            gravity_active = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click happened inside the book's rectangle
            if book_img.get_rect().collidepoint(event.pos):
                show_collection(screen)
                collection = not collection
        
        if event.type == pygame.MOUSEBUTTONDOWN and collection:
            for rects in badges_rects:
                if rects is not None and rects.collidepoint(event.pos):
                    show_card = FusionCards.Popup(atoms_symbols[badges_rects.index(rects)], 150, 300)
                    show_card.is_visible = True
                    cards.append(show_card)


        # Camera Controls
        keys = pygame.key.get_pressed()
        
        #reset the camera zoom
        if keys[pygame.K_r]:
            camera_zoom = DEFAULT_ZOOM
        
        #toggle between whether the camera follows your mouse or not
        if keys[pygame.K_f]:
            if follow_mode:
                follow_mode = False
            else:
                follow_mode = True
        # Zoom in & out
        if event.type == pygame.MOUSEWHEEL and not collection:
            if event.y > 0:
                zoom_at(pygame.mouse.get_pos(), ZOOM_STEP)
            elif event.y < 0:
                zoom_at(pygame.mouse.get_pos(), 1 / ZOOM_STEP)
                
        #music control
        #toggle music with M key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                follow_mode = not follow_mode
    
            if event.key == pygame.K_m:  # Toggle music with M key
                music_on = not music_on
                if music_on:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

    if follow_mode and not collection:
        cursor_follow_camera(pygame.mouse.get_pos())
    else:
        camera_x,camera_y = screen_to_world((WIDTH/2,HEIGHT/2))
    clamp_camera()


    if gravity_active:
        gravity_pos = screen_to_world(pygame.mouse.get_pos())


    for p in particles:
        p.draw(screen)
        # if isinstance(p, Nucleon) and p.name == "H-1":
            # apply_cluster_attraction(p, particles)

    for popups in popup:
        if popups.is_visible:
            popups.draw(screen)


    if collection:
        show_collection(screen)
        for card in cards:
            card.draw(screen)
    else:
        # ---------Creates sound when hold mouse pad-----------
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # If Left Mouse is held down
            if not pygame.mixer.get_busy():  # Only play if sound isn't already playing
                # -1 tells it to loop until we call stop()
                channel = tone.play(loops=-1)
        else:
            # If the mouse is released, stop the sound
            tone.fadeout(500)
            '''if channel:
                channel.stop()'''

        handle_collisions()

        for p in particles:
            p.update()

        if gravity_active:
            mx, my = world_to_screen(gravity_pos)
            outer_radius = max(1, int(25 * camera_zoom))
            inner_radius = max(1, int(5 * camera_zoom))
            pygame.draw.circle(screen, (180, 180, 255), (mx, my), outer_radius, 2)
            pygame.draw.circle(screen, (120, 120, 255), (mx, my), inner_radius)

        check_quarks_merging()
        check_atom_merging()

    screen.blit(book_img, (20,20))

    fps_value = clock.get_fps()
    fps_text = font.render(f"FPS: {fps_value:.2f}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()

pygame.quit()