import pygame

# Define colors (RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
FPS = 30

class piece:
    def __init__(self, name, valid_moves, start_pos):
        piece.name = name
        piece.valid_moves = valid_moves
        piece.start_pos = start_pos

def main():
    # Import and Initialize Pygame
    pygame.init()

    # Set Up the Display
    screen_width = 600
    screen_height = 600
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chess")
    window.fill((255, 255, 255))

    # Creates checkerboard pattern
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                x = col * 75
                y = row * 75
                pygame.draw.rect(window, BLACK, (x, y, 75, 75))
    pygame.display.update()

    # Adds white pawn and black pawn images to game set
    wpa = pygame.image.load("wp.png").convert_alpha()
    wpa = pygame.transform.scale(wpa, (75, 75))
    wpb = pygame.image.load("wp.png").convert_alpha()
    wpb = pygame.transform.scale(wpb, (75, 75))
    wpc = pygame.image.load("wp.png").convert_alpha()
    wpc = pygame.transform.scale(wpb, (75, 75))
    wpd = pygame.image.load("wp.png").convert_alpha()
    wpd = pygame.transform.scale(wpb, (75, 75))
    wpe = pygame.image.load("wp.png").convert_alpha()
    wpe = pygame.transform.scale(wpb, (75, 75))
    wpf = pygame.image.load("wp.png").convert_alpha()
    wpf = pygame.transform.scale(wpb, (75, 75))
    wpg = pygame.image.load("wp.png").convert_alpha()
    wpg = pygame.transform.scale(wpb, (75, 75))
    wph = pygame.image.load("wp.png").convert_alpha()
    wph = pygame.transform.scale(wpb, (75, 75))
    

    # Sets objects on board
    wpa_hitbox = pygame.Rect(0, 75, 75, 75)
    wpb_hitbox = pygame.Rect(75, 75, 75, 75)
    wpc_hitbox = pygame.Rect(150, 75, 75, 75)
    wpd_hitbox = pygame.Rect(225, 75, 75, 75)
    wpe_hitbox = pygame.Rect(300, 75, 75, 75)
    wpf_hitpox = pygame.Rect(375, 75, 75, 75)
    wpg_hitbox = pygame.Rect(450, 75, 75, 75)
    wph_hitbox = pygame.Rect(525, 75, 75, 75)
    is_dragging = False
    offset = (0, 0)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Checks if left mouse is pressed
                    if wpa_hitbox.collidepoint(event.pos): # Allows object to be dragged
                        is_dragging = True
                        mouse_x, mouse_y = event.pos
                        offset = (wpa_hitbox.x - mouse_x, wpa_hitbox.y - mouse_y)
            elif event.type == pygame.MOUSEBUTTONUP: # Stops dragging operation
                if event.button == 1:
                    is_dragging = False
            elif event.type == pygame.MOUSEMOTION: # Dragging math
                if is_dragging:
                    mouse_x, mouse_y = event.pos
                    wpa_hitbox.x = mouse_x + offset[0]
                    wpa_hitbox.y = mouse_y + offset[1]

        # Redraw board
        window.fill(WHITE)
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(window, BLACK, (col * 75, row * 75, 75, 75))

        # Draw sprite
        window.blit(wpa, wpa_hitbox)
        window.blit(wpb, wpb_hitbox)
        window.blit(wpc, wpc_hitbox)
        window.blit(wpd, wpd_hitbox)
        window.blit(wpe, wpe_hitbox)
        window.blit(wpf, wpf_hitpox)
        window.blit(wpg, wpg_hitbox)
        window.blit(wph, wph_hitbox)

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

main()