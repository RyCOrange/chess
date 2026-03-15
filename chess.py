import pygame

pygame.init()

# Define colors (RGB values) and frame rates
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
LT_GREEN = (144, 238, 144)
LT_RED = (255, 128, 128)

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
    
# Rotates the board
def transform(x, y, rotated):
    """Flip coordinates 180° around board center if rotated."""
    if rotated:
        return 525 - x, 525 - y  # 525 = 7 * 75
    return x, y

def get_image(piece_type, rotated):
    img = images[piece_type].copy()
    if rotated:
        return pygame.transform.rotate(img, 180)
    return img

# Sets up general chess piece class
class chess_piece(pygame.sprite.Sprite):
    def __init__(self, piece_type, name, x, y):
        super().__init__()
        self.name = name
        self.piece_type = piece_type
        self.image = images[piece_type].copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset = (0, 0)

    def valid_moves(self, all_pieces):
        col = self.rect.x // 75
        row = self.rect.y // 75

        occupied = {(p.rect.x // 75, p.rect.y // 75): p for p in all_pieces if p != self}

        # White pawn movement instructions
        if self.piece_type == "WP":
            moves = []
            one_ahead = (col, row - 1)
            two_ahead = (col, row - 2)

            # Can only move forward if square is empty
            if one_ahead not in occupied:
                moves.append(one_ahead)
                # Two square advance only from starting row and if path is clear
                if row == 6 and two_ahead not in occupied:
                    moves.append(two_ahead)

            # Diagonal captures - only if an enemy piece is there
            for capture_col in [col - 1, col + 1]:
                target = (capture_col, row - 1)
                if target in occupied and occupied[target].piece_type.startswith("B"):
                    moves.append(target)
            
            return moves, occupied

        if self.piece_type == "WN":
            wn_moves = [(col - 1, row - 2), (col - 2, row - 1), (col + 1, row - 2), (col - 1, row + 2), 
                        (col + 1, row + 2), (col - 2, row + 1), (col + 2, row + 1), (col + 2, row - 1)]
            moves = []
            for target in wn_moves:
                if target not in occupied:
                    moves.append(target)  # Empty square, valid move
                elif occupied[target].piece_type.startswith("B"):
                    moves.append(target)  # Enemy piece, valid capture
                # If friendly piece, do nothing (blocked)
            return moves, occupied
        
        # Pawn movement instructions
        if self.piece_type == "BP":
            moves = []
            one_ahead = (col, row + 1)
            two_ahead = (col, row + 2)

            # Can only move forward if square is empty
            if one_ahead not in occupied:
                moves.append(one_ahead)
                # Two square advance only from starting row and if path is clear
                if row == 2 and two_ahead not in occupied:
                    moves.append(two_ahead)

            # Diagonal captures - only if an enemy piece is there
            for capture_col in [col + 1, col - 1]:
                target = (capture_col, row + 1)
                if target in occupied and occupied[target].piece_type.startswith("W"):
                    moves.append(target)
            
            return moves, occupied

        if self.piece_type == "BN":
            wn_moves = [(col - 1, row - 2), (col - 2, row - 1), (col + 1, row - 2), (col - 1, row + 2), 
                        (col + 1, row + 2), (col - 2, row + 1), (col + 2, row + 1), (col + 2, row - 1)]
            moves = []
            for target in wn_moves:
                if target not in occupied:
                    moves.append(target)  # Empty square, valid move
                elif occupied[target].piece_type.startswith("W"):
                    moves.append(target)  # Enemy piece, valid capture
                # If friendly piece, do nothing (blocked)
            return moves, occupied

    def promote(self, new_type):
        self.piece_type = new_type
        self.image = images[new_type].copy()

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
    w_pawns = {name: chess_piece("WP", name, x, y) for name, (x, y) in w_pawn_data.items()}
    w_rook_data = {"wra": (0, 525), "wrh": (525, 525)}
    w_rooks = {name: chess_piece("WR", name, x, y) for name, (x, y) in w_rook_data.items()}
    w_knight_data = {"wnb": (75, 525), "wng": (450, 525)}
    w_knights = {name: chess_piece("WN", name, x, y) for name, (x, y) in w_knight_data.items()}
    w_bishop_data = {"wbc": (150, 525), "wbf": (375, 525)}
    w_bishops = {name: chess_piece("WB", name, x, y) for name, (x, y) in w_bishop_data.items()}
    w_queen_data = {"wqd": (225, 525)}
    w_queens = {name: chess_piece("WQ", name, x, y) for name, (x, y) in w_queen_data.items()}
    w_king_data = {"wke": (300, 525)}
    w_kings = {name: chess_piece("WK", name, x, y) for name, (x, y) in w_king_data.items()}

    # Black pieces
    b_pawn_data = {"bpa": (0, 75), "bpb": (75, 75), "bpc": (150, 75), "bpd": (225, 75), 
                   "bpe": (300, 75), "bpf": (375, 75), "bpg": (450, 75), "bph": (525, 75)}
    b_pawns = {name: chess_piece("BP", name, x, y) for name, (x, y) in b_pawn_data.items()}
    b_rook_data = {"bra": (0, 0), "brh": (525, 0)}
    b_rooks = {name: chess_piece("BR", name, x, y) for name, (x, y) in b_rook_data.items()}
    b_knight_data = {"bnb": (75, 0), "bng": (450, 0)}
    b_knights = {name: chess_piece("BN", name, x, y) for name, (x, y) in b_knight_data.items()}
    b_bishop_data = {"bbc": (150, 0), "bbf": (375, 0)}
    b_bishops = {name: chess_piece("BB", name, x, y) for name, (x, y) in b_bishop_data.items()}
    b_queen_data = {"bqd": (225, 0)}
    b_queens = {name: chess_piece("BQ", name, x, y) for name, (x, y) in b_queen_data.items()}
    b_king_data = {"bke": (300, 0)}
    b_kings = {name: chess_piece("BK", name, x, y) for name, (x, y) in b_king_data.items()}

    all_pieces = (list(w_pawns.values()) + list(w_rooks.values()) + list(w_knights.values()) 
                  + list(w_bishops.values()) + list(w_queens.values()) + list(w_kings.values()) 
                  + list(b_pawns.values()) + list(b_rooks.values()) + list(b_knights.values()) 
                  + list(b_bishops.values()) + list(b_queens.values()) + list(b_kings.values()))

    running = True
    clock = pygame.time.Clock()
    selected_piece = None
    white_turn = True
    rotated = False
    valid_moves = []
    occupied = {}
    promoting = False
    promoting_piece = None
    #######################
    # Begin gameplay loop #
    #######################
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Piece movement
            elif event.type == pygame.MOUSEBUTTONDOWN: # Initiates drag
                mx, my = transform(event.pos[0], event.pos[1], rotated)
                if event.button == 1:
                    if promoting:
                        for i, option in enumerate(["WQ", "WR", "WB", "WN"]):
                            if pygame.Rect(i * 75, 262, 75, 75).collidepoint(event.pos):
                                promoting_piece.promote(option)
                                promoting = False
                                break
                    else:
                        for piece in reversed(all_pieces):
                            if piece.rect.collidepoint(mx, my):
                                if (white_turn and piece.piece_type.startswith("W")) or \
                                    (not white_turn and piece.piece_type.startswith("B")):
                                        piece.dragging = True
                                        piece.offset = (piece.rect.x - mx, piece.rect.y - my)
                                        piece.origin = (piece.rect.x, piece.rect.y)
                                        valid_moves, occupied = piece.valid_moves(all_pieces)
                                        break
                

            elif event.type == pygame.MOUSEBUTTONUP: # Stops dragging
                if event.button == 1:
                    for piece in all_pieces:
                        if piece.dragging:
                            # Snap to nearest square by rounding to nearest 75px
                            col = round(piece.rect.x / 75)
                            row = round(piece.rect.y / 75)
                            # Activates pawn promotion
                            if piece.piece_type == "WP" and row == 0:
                                promoting = True
                                promoting_piece = piece
                            elif piece.piece_type == "BP" and row == 7:
                                promoting = True
                                promoting_piece = piece

                            # Clamp to board boundaries (0–7)
                            col = max(0, min(7, col))
                            row = max(0, min(7, row))

                            # Apply snapped position
                            if (col, row) in valid_moves:
                                for target_piece in all_pieces[:]:  # [:] to safely remove while iterating
                                    if (target_piece.rect.x // 75 == col and 
                                        target_piece.rect.y // 75 == row and 
                                        target_piece != piece):
                                        all_pieces.remove(target_piece)  # Remove captured piece
                                        break
                                piece.rect.x = col * 75
                                piece.rect.y = row * 75
                                white_turn = not white_turn
                                rotated = not rotated
                            else:
                                piece.rect.x, piece.rect.y = piece.origin

                        piece.dragging = False
                    valid_moves = []

            elif event.type == pygame.MOUSEMOTION: # Moves piece while dragging
                mx, my = transform(event.pos[0], event.pos[1], rotated)
                for piece in all_pieces:
                    if piece.dragging:
                        piece.rect.x = mx + piece.offset[0]
                        piece.rect.y = my + piece.offset[1]

        ##################
        # Redraw Objects #
        ##################
        # Redraw board
        window.fill(WHITE)
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(window, BLACK, (col * 75, row * 75, 75, 75))

        # Draws pieces during movement
        for piece in all_pieces:
            dx, dy = transform(piece.rect.x, piece.rect.y, rotated)
            window.blit(piece.image, (dx, dy))

        # Highlights valid move location
        for (col, row) in valid_moves:
            dx, dy = transform(col * 75, row * 75, rotated)
            target = (col, row)
            if target in occupied and occupied[target]:
                pygame.draw.rect(window, LT_RED, (dx, dy, 75, 75))
            else:
                pygame.draw.rect(window, LT_GREEN, (dx, dy, 75, 75))
        
        if promoting:
            for i, option in enumerate(["WQ", "WR", "WB", "WN"]):
                pygame.draw.rect(window, WHITE, (i * 75, 262, 75, 75))
                window.blit(images[option], (i * 75, 262))

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

main()