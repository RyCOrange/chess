import pygame

# Define colors (RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
FPS = 30

class w_pawn(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = WP_IMAGE.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset = (0, 0)

class b_pawn(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = BP_IMAGE.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset = (0, 0)

def main():
    # Initialize Pygame
    pygame.init()

    # Set Up the Display
    screen_width = 600
    screen_height = 600
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chess")
    window.fill((255, 255, 255))

    # Define piece images
    global WP_IMAGE
    WP_IMAGE = pygame.transform.scale(pygame.image.load("wp.png").convert_alpha(), (75, 75))
    global BP_IMAGE
    BP_IMAGE = pygame.transform.scale(pygame.image.load("bp.png").convert_alpha(), (75, 75))

    # Creates checkerboard pattern
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                x = col * 75
                y = row * 75
                pygame.draw.rect(window, BLACK, (x, y, 75, 75))
    pygame.display.update()

    # Adds white pawns to game board
    w_pawn_data = {"wpa": (0, 450), "wpb": (75, 450), "wpc": (150, 450), "wpd": (225, 450), "wpe": (300, 450), "wpf": (375, 450),
                   "wpg": (450, 450), "wph": (525, 450)}
    w_pawns = {name: w_pawn(name, x, y) for name, (x, y) in w_pawn_data.items()}

    # Adds black pawns to game board
    b_pawn_data = {"bpa": (0, 75), "bpb": (75, 75), "bpc": (150, 75), "bpd": (225, 75), "bpe": (300, 75), "bpf": (375, 75),
                   "bpg": (450, 75), "bph": (525, 75)}
    b_pawns = {name: b_pawn(name, x, y) for name, (x, y) in b_pawn_data.items()}

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Pawn movement
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    all_pawns = list(w_pawns.values()) + list(b_pawns.values())
                    for pawn in reversed(all_pawns):
                        if pawn.rect.collidepoint(event.pos):
                            pawn.dragging = True
                            pawn.offset = (pawn.rect.x - event.pos[0], pawn.rect.y - event.pos[1])
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for pawn in list(w_pawns.values()) + list(b_pawns.values()):
                        pawn.dragging = False

            elif event.type == pygame.MOUSEMOTION:
                for pawn in list(w_pawns.values()) + list(b_pawns.values()):
                    if pawn.dragging:
                        pawn.rect.x = event.pos[0] + pawn.offset[0]
                        pawn.rect.y = event.pos[1] + pawn.offset[1]


        # Redraw board
        window.fill(WHITE)
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(window, BLACK, (col * 75, row * 75, 75, 75))

        for pawn in w_pawns.values():
            window.blit(pawn.image, pawn.rect)
        for pawn in b_pawns.values():
            window.blit(pawn.image, pawn.rect)

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

main()