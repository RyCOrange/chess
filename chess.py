import pygame

# Define colors (RGB values) and frame rates
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

class w_rook(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = WR_IMAGE.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset = (0, 0)

class w_knight(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = WN_IMAGE.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset = (0, 0)

class w_bishop(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = WB_IMAGE.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset = (0, 0)

class w_queen(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = WQ_IMAGE.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset = (0, 0)

class w_king(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = WK_IMAGE.copy()
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
    image_size = (75, 75)
    global WP_IMAGE
    WP_IMAGE = pygame.transform.scale(pygame.image.load("wp.png").convert_alpha(), image_size)
    global WR_IMAGE
    WR_IMAGE = pygame.transform.scale(pygame.image.load("wr.png").convert_alpha(), image_size)
    global WN_IMAGE
    WN_IMAGE = pygame.transform.scale(pygame.image.load("wn.png").convert_alpha(), image_size)
    global WB_IMAGE
    WB_IMAGE = pygame.transform.scale(pygame.image.load("wb.png").convert_alpha(), image_size)
    global WQ_IMAGE
    WQ_IMAGE = pygame.transform.scale(pygame.image.load("wq.png").convert_alpha(), image_size)
    global WK_IMAGE
    WK_IMAGE = pygame.transform.scale(pygame.image.load("wk.png").convert_alpha(), image_size)
    global BP_IMAGE
    BP_IMAGE = pygame.transform.scale(pygame.image.load("bp.png").convert_alpha(), image_size)

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

    # Adds white rooks to game board
    w_rook_data = {"wra": (0, 525), "wrh": (525, 525)}
    w_rooks = {name: w_rook(name, x, y) for name, (x, y) in w_rook_data.items()}

    # Adds white knights to game board
    w_knight_data = {"wnb": (75, 525), "wng": (450, 525)}
    w_knights = {name: w_knight(name, x, y) for name, (x, y) in w_knight_data.items()}

    # Adds white bishops to game board
    w_bishop_data = {"wbc": (150, 525), "wbf": (375, 525)}
    w_bishops = {name: w_bishop(name, x, y) for name, (x, y) in w_bishop_data.items()}

    # Adds white queen to game board
    w_queen_data = {"wqd": (225, 525)}
    w_queens = {name: w_queen(name, x, y) for name, (x, y) in w_queen_data.items()}

    # Adds white king to game board
    w_king_data = {"wke": (300, 525)}
    w_kings = {name: w_king(name, x, y) for name, (x, y) in w_king_data.items()}

    # Adds black pawns to game board
    b_pawn_data = {"bpa": (0, 75), "bpb": (75, 75), "bpc": (150, 75), "bpd": (225, 75), "bpe": (300, 75), "bpf": (375, 75),
                   "bpg": (450, 75), "bph": (525, 75)}
    b_pawns = {name: b_pawn(name, x, y) for name, (x, y) in b_pawn_data.items()}

    all_pieces = (list(w_pawns.values()) + list(w_rooks.values()) + list(w_knights.values()) 
                  + list(w_bishops.values()) + list(w_queens.values()) + list(w_kings.values()) + list(b_pawns.values()))

    running = True
    clock = pygame.time.Clock()
    # Begin gameplay loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Piece movement
            elif event.type == pygame.MOUSEBUTTONDOWN: # Initiates drag
                if event.button == 1:
                    for piece in reversed(all_pieces):
                        if piece.rect.collidepoint(event.pos):
                            piece.dragging = True
                            piece.offset = (piece.rect.x - event.pos[0], piece.rect.y - event.pos[1])
                            break

            elif event.type == pygame.MOUSEBUTTONUP: # Stops drag
                if event.button == 1:
                    for piece in all_pieces:
                        piece.dragging = False

            elif event.type == pygame.MOUSEMOTION: # Moves piece while dragging
                for piece in all_pieces:
                    if piece.dragging:
                        piece.rect.x = event.pos[0] + piece.offset[0]
                        piece.rect.y = event.pos[1] + piece.offset[1]


        # Redraw board
        window.fill(WHITE)
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(window, BLACK, (col * 75, row * 75, 75, 75))

        for piece in all_pieces:
            window.blit(piece.image, piece.rect)

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

main()