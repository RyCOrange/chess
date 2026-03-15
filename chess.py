import pygame

pygame.init()

# Define colors (RGB values) and frame rates
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
FPS = 30

images = {}  # Empty global dict

# Loads images tied to piece ID
def load_images():
    """Call this once after pygame.display.set_mode()"""
    global images
    image_size = (75, 75)
    image_files = {
        "WP": "wp.png", "WR": "wr.png", "WN": "wn.png",
        "WB": "wb.png", "WQ": "wq.png", "WK": "wk.png",
        "BP": "bp.png", "BR": "br.png", "BN": "bn.png",
        "BB": "bb.png", "BQ": "bq.png", "BK": "bk.png"
    }
    images = {name: pygame.transform.scale(pygame.image.load(file).convert_alpha(), image_size)
              for name, file in image_files.items()}

# Sets up general chess piece class
class chess_piece(pygame.sprite.Sprite):
    def __init__(self, piece_type, name, x, y):
        super().__init__()
        self.name = name
        self.image = images[piece_type].copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset = (0, 0)

def main():
    # Set Up the Display
    window = pygame.display.set_mode((600, 600))
    load_images()
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

    # White pieces
    w_pawn_data = {"wpa": (0, 450), "wpb": (75, 450), "wpc": (150, 450), "wpd": (225, 450), 
                   "wpe": (300, 450), "wpf": (375, 450), "wpg": (450, 450), "wph": (525, 450)}
    w_pawns   = {name: chess_piece("WP", name, x, y) for name, (x, y) in w_pawn_data.items()}
    w_rook_data = {"wra": (0, 525), "wrh": (525, 525)}
    w_rooks   = {name: chess_piece("WR", name, x, y) for name, (x, y) in w_rook_data.items()}
    w_knight_data = {"wnb": (75, 525), "wng": (450, 525)}
    w_knights = {name: chess_piece("WN", name, x, y) for name, (x, y) in w_knight_data.items()}
    w_bishop_data = {"wbc": (150, 525), "wbf": (375, 525)}
    w_bishops = {name: chess_piece("WB", name, x, y) for name, (x, y) in w_bishop_data.items()}
    w_queen_data = {"wqd": (225, 525)}
    w_queens  = {name: chess_piece("WQ", name, x, y) for name, (x, y) in w_queen_data.items()}
    w_king_data = {"wke": (300, 525)}
    w_kings   = {name: chess_piece("WK", name, x, y) for name, (x, y) in w_king_data.items()}

    # Black pieces
    b_pawn_data = {"bpa": (0, 75), "bpb": (75, 75), "bpc": (150, 75), "bpd": (225, 75), 
                   "bpe": (300, 75), "bpf": (375, 75), "bpg": (450, 75), "bph": (525, 75)}
    b_pawns   = {name: chess_piece("BP", name, x, y) for name, (x, y) in b_pawn_data.items()}
    b_rook_data = {"bra": (0, 0), "brh": (525, 0)}
    b_rooks   = {name: chess_piece("BR", name, x, y) for name, (x, y) in b_rook_data.items()}
    b_knight_data = {"bnb": (75, 0), "bng": (450, 0)}
    b_knights = {name: chess_piece("BN", name, x, y) for name, (x, y) in b_knight_data.items()}
    b_bishop_data = {"bbc": (150, 0), "bbf": (375, 0)}
    b_bishops = {name: chess_piece("BB", name, x, y) for name, (x, y) in b_bishop_data.items()}
    b_queen_data = {"bqd": (225, 0)}
    b_queens  = {name: chess_piece("BQ", name, x, y) for name, (x, y) in b_queen_data.items()}
    b_king_data = {"bke": (300, 0)}
    b_kings   = {name: chess_piece("BK", name, x, y) for name, (x, y) in b_king_data.items()}

    all_pieces = (list(w_pawns.values()) + list(w_rooks.values()) + list(w_knights.values()) 
                  + list(w_bishops.values()) + list(w_queens.values()) + list(w_kings.values()) 
                  + list(b_pawns.values()) + list(b_rooks.values()) + list(b_knights.values()) 
                  + list(b_bishops.values()) + list(b_queens.values()) + list(b_kings.values()))

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