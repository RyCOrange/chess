import pygame
import time

pygame.init()

# Define colors (RGB values) and frame rates
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)

FPS = 30

images = {}  # Empty global dict

# Loads images tied to piece ID
def load_images():
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

#################
# Check testing #
#################

# Tests if king is in check
def is_in_check(all_pieces, white_king_turn):
    prefix = "W" if white_king_turn else "B"
    enemy_prefix = "B" if white_king_turn else "W"

    # Find the current player's king
    king = next((p for p in all_pieces if p.piece_type == f"{prefix}K"), None)
    if not king:
        return False
    king_pos = (king.rect.x // 75, king.rect.y // 75)

    # Check if any enemy piece can attack the king's square
    for piece in all_pieces:
        if piece.piece_type.startswith(enemy_prefix):
            moves, _, _, _ = piece.valid_moves(all_pieces, turn_number=0)
            if king_pos in moves:
                return True
    return False

# Simulates next move to see if king will be in check
def move_leaves_king_in_check(piece, target_col, target_row, all_pieces, white_turn):
    import copy

    # Make shallow copies of pieces but ensure each has its own Rect
    sim_pieces = []
    for p in all_pieces:
        sp = copy.copy(p)
        try:
            sp.rect = p.rect.copy()
        except Exception:
            sp.rect = pygame.Rect(p.rect)
        sim_pieces.append(sp)

    # Find the corresponding piece in the simulation
    sim_piece = next(p for p in sim_pieces if p.name == piece.name)

    # Remove any captured piece from simulation
    sim_pieces = [p for p in sim_pieces
                  if not (p.rect.x // 75 == target_col and
                          p.rect.y // 75 == target_row and
                          p != sim_piece)]

    # Apply the move to the simulated piece only
    sim_piece.rect.x = target_col * 75
    sim_piece.rect.y = target_row * 75

    return is_in_check(sim_pieces, white_turn)

# Sends only moves to keep king out of check
def get_legal_moves(piece, all_pieces, white_turn, turn_number):
    moves, occupied, castling_moves, en_passant_moves = piece.valid_moves(all_pieces, turn_number)
    legal = [m for m in moves
             if not move_leaves_king_in_check(piece, m[0], m[1], all_pieces, white_turn)]
    return legal, occupied, castling_moves, en_passant_moves

# Checkmate condition
def is_checkmate(all_pieces, white_turn, turn_number):
    """Returns True if the current player has no legal moves and is in check."""
    if not is_in_check(all_pieces, white_turn):
        return False  # Not in check, so can't be checkmate (could be stalemate)

    prefix = "W" if white_turn else "B"
    for piece in all_pieces:
        if piece.piece_type.startswith(prefix):
            legal, _, _, _ = get_legal_moves(piece, all_pieces, white_turn, turn_number)
            if legal:
                return False  # Found at least one legal move
    return True

###############
# Piece Setup #
###############

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
        self.move_counter = 0
        self.last_double_advance_turn = -1

    def valid_moves(self, all_pieces, turn_number):
        col = self.rect.x // 75
        row = self.rect.y // 75

        occupied = {(p.rect.x // 75, p.rect.y // 75): p for p in all_pieces if p != self}

        ################
        # White pieces #
        ################
        # White pawn movement
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
            # en Passant
            en_passant_moves = set()
            b_pawn_l = occupied.get((col - 1, row))
            b_pawn_r = occupied.get((col + 1, row))
            if b_pawn_l and b_pawn_l.piece_type == "BP" and b_pawn_l.last_double_advance_turn == turn_number - 1:
                en_passant_moves.add((col - 1, row - 1))
                moves.append((col - 1, row - 1))
            elif b_pawn_r and b_pawn_r.piece_type == "BP" and b_pawn_r.last_double_advance_turn == turn_number - 1:
                en_passant_moves((col + 1, row - 1))
                moves.append((col + 1, row - 1))
            
            return moves, occupied, set(), en_passant_moves

        # White knight movement
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
            return moves, occupied, set(), set()
        
        # White queen movement
        if self.piece_type == "WQ":
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1),   # rook directions
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]   # bishop directions
            moves = []
            for dx, dy in directions:
                cx, cy = col + dx, row + dy
                while 0 <= cx <= 7 and 0 <= cy <= 7:
                    if (cx, cy) in occupied:
                        if occupied[(cx, cy)].piece_type.startswith("B"):
                            moves.append((cx, cy))  # Can capture enemy
                        break  # Blocked by any piece (friendly or enemy)
                    moves.append((cx, cy))  # Empty square
                    cx += dx
                    cy += dy
            return moves, occupied, set(), set()
        
        # White rook movement
        if self.piece_type == "WR":
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # rook directions
            moves = []
            for dx, dy in directions:
                cx, cy = col + dx, row + dy
                while 0 <= cx <= 7 and 0 <= cy <= 7:
                    if (cx, cy) in occupied:
                        if occupied[(cx, cy)].piece_type.startswith("B"):
                            moves.append((cx, cy))  # Can capture enemy
                        break  # Blocked by any piece (friendly or enemy)
                    moves.append((cx, cy))  # Empty square
                    cx += dx
                    cy += dy
            return moves, occupied, set(), set()
        
        # White bishop movement
        if self.piece_type == "WB":
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]   # bishop directions
            moves = []
            for dx, dy in directions:
                cx, cy = col + dx, row + dy
                while 0 <= cx <= 7 and 0 <= cy <= 7:
                    if (cx, cy) in occupied:
                        if occupied[(cx, cy)].piece_type.startswith("B"):
                            moves.append((cx, cy))  # Can capture enemy
                        break  # Blocked by any piece (friendly or enemy)
                    moves.append((cx, cy))  # Empty square
                    cx += dx
                    cy += dy
            return moves, occupied, set(), set()
        
        # White king movement
        if self.piece_type == "WK":
            wk_moves = [(col - 1, row - 1), (col + 1, row + 1), (col + 1, row - 1), (col - 1, row + 1), (col, row + 1),
                        (col + 1, row), (col, row - 1), (col - 1, row), (col + 1, row)]
            moves = []
            for target in wk_moves:
                if target not in occupied:
                    moves.append(target)  # Empty square, valid move
                elif occupied[target].piece_type.startswith("B"):
                    moves.append(target)  # Enemy piece, valid capture
                # If friendly piece, do nothing (blocked)
            # Kingside castling
            castling_moves = set()
            if self.move_counter == 0:
                rook = occupied.get((7, 7))
                if rook and rook.piece_type == "WR" and rook.move_counter == 0:
                    if (6, 7) not in occupied and (5, 7) not in occupied:
                        moves.append((6, 7))
                        castling_moves.add((6, 7))
                # Queenside Castling
                rook = occupied.get((0, 7))
                if rook and rook.piece_type == "WR" and rook.move_counter == 0:
                    if (1, 7) not in occupied and (2, 7) not in occupied and (3, 7) not in occupied:
                        moves.append((2, 7))
                        castling_moves.add((2, 7))
            return moves, occupied, castling_moves, set()
        
        ################
        # Black pieces #
        ################
        # Black pawn movement
        if self.piece_type == "BP":
            moves = []
            one_ahead = (col, row + 1)
            two_ahead = (col, row + 2)

            # Can only move forward if square is empty
            if one_ahead not in occupied:
                moves.append(one_ahead)
                # Two square advance only from starting row and if path is clear
                if row == 1 and two_ahead not in occupied:
                    moves.append(two_ahead)

            # Diagonal captures - only if an enemy piece is there
            for capture_col in [col + 1, col - 1]:
                target = (capture_col, row + 1)
                if target in occupied and occupied[target].piece_type.startswith("W"):
                    moves.append(target)

            # en Passant
            en_passant_moves = set()
            w_pawn_l = occupied.get((col - 1, row))
            w_pawn_r = occupied.get((col + 1, row))
            if w_pawn_l and w_pawn_l.piece_type == "WP" and w_pawn_l.last_double_advance_turn == turn_number - 1:
                en_passant_moves.add((col - 1, row + 1))
                moves.append((col - 1, row + 1))
            elif w_pawn_r and w_pawn_r.piece_type == "WP" and w_pawn_r.last_double_advance_turn == turn_number - 1:
                en_passant_moves.add((col + 1, row + 1))
                moves.append((col + 1, row + 1))
            
            return moves, occupied, set(), en_passant_moves

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
            return moves, occupied, set(), set()
    
        # Black queen movement
        if self.piece_type == "BQ":
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1),   # rook directions
                (1, 1), (1, -1), (-1, 1), (-1, -1)]   # bishop directions
            moves = []
            for dx, dy in directions:
                cx, cy = col + dx, row + dy
                while 0 <= cx <= 7 and 0 <= cy <= 7:
                    if (cx, cy) in occupied:
                        if occupied[(cx, cy)].piece_type.startswith("W"):
                            moves.append((cx, cy))  # Can capture enemy
                        break  # Blocked by any piece (friendly or enemy)
                    moves.append((cx, cy))  # Empty square
                    cx += dx
                    cy += dy
            return moves, occupied, set(), set()
        
        # Black rook movement
        if self.piece_type == "BR":
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # rook directions
            moves = []
            for dx, dy in directions:
                cx, cy = col + dx, row + dy
                while 0 <= cx <= 7 and 0 <= cy <= 7:
                    if (cx, cy) in occupied:
                        if occupied[(cx, cy)].piece_type.startswith("W"):
                            moves.append((cx, cy))  # Can capture enemy
                        break  # Blocked by any piece (friendly or enemy)
                    moves.append((cx, cy))  # Empty square
                    cx += dx
                    cy += dy
            return moves, occupied, set(), set()
        
        # Black bishop movement
        if self.piece_type == "BB":
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]   # bishop directions
            moves = []
            for dx, dy in directions:
                cx, cy = col + dx, row + dy
                while 0 <= cx <= 7 and 0 <= cy <= 7:
                    if (cx, cy) in occupied:
                        if occupied[(cx, cy)].piece_type.startswith("W"):
                            moves.append((cx, cy))  # Can capture enemy
                        break  # Blocked by any piece (friendly or enemy)
                    moves.append((cx, cy))  # Empty square
                    cx += dx
                    cy += dy
            return moves, occupied, set(), set()
        
        # Black king moves
        if self.piece_type == "BK":
            bk_moves = [(col - 1, row - 1), (col + 1, row + 1), (col + 1, row - 1), (col - 1, row + 1), (col, row + 1),
                        (col + 1, row), (col, row - 1), (col - 1, row), (col + 1, row)]
            moves = []
            for target in bk_moves:
                if target not in occupied:
                    moves.append(target)  # Empty square, valid move
                elif occupied[target].piece_type.startswith("W"):
                    moves.append(target)  # Enemy piece, valid capture
                # If friendly piece, do nothing (blocked)
            castling_moves = set()
            if self.move_counter == 0:
                # Kingside castling
                rook = occupied.get((7, 0))
                if rook and rook.piece_type == "BR" and rook.move_counter == 0:
                    if (6, 0) not in occupied and (5, 0) not in occupied:
                        moves.append((6, 0))
                        castling_moves.add((6, 0))
                # Queenside castling
                rook = occupied.get((0, 0))
                if rook and rook.piece_type == "BR" and rook.move_counter == 0:
                    if (1, 0) not in occupied and (2, 0) not in occupied and (3, 0) not in occupied:
                        moves.append((2, 0))
                        castling_moves.add((2, 0))
            return moves, occupied, castling_moves, set()
        return [], occupied, castling_moves, en_passant_moves

    def promote(self, new_type):
        self.piece_type = new_type
        self.image = images[new_type].copy()

########
# main #
########
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


    ####################
    # Piece Definition #
    ####################
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

    #####################
    # Pre-game settings #
    #####################
    font = pygame.font.SysFont(None, 60)
    in_check = False
    game_over = False
    running = True
    clock = pygame.time.Clock()
    selected_piece = None
    white_turn = True
    turn_number = 0
    rotated = False
    valid_moves = []
    occupied = {}
    en_passant_moves = set()
    castling_moves = set()
    promoting = False
    promoting_piece = None
    castling = False
    castling_king = None
    #######################
    # Begin gameplay loop #
    #######################
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            ########################
            # Mouse button pressed #
            ########################
            elif event.type == pygame.MOUSEBUTTONDOWN: # Initiates drag
                if not game_over:
                    if event.button == 1:
                        if promoting:
                            options = ["WQ", "WR", "WB", "WN"] if promoting_piece.piece_type == "WP" else ["BQ", "BR", "BB", "BN"]
                            for i, option in enumerate(options):
                                if pygame.Rect(i * 75, 262, 75, 75).collidepoint(event.pos):
                                    promoting_piece.promote(option)
                                    promoting = False
                                    break
                        else:
                            for piece in reversed(all_pieces):
                                dx, dy = transform(piece.rect.x, piece.rect.y, rotated)
                                if pygame.Rect(dx, dy, 75, 75).collidepoint(event.pos):
                                    if (white_turn and piece.piece_type.startswith("W")) or \
                                        (not white_turn and piece.piece_type.startswith("B")):
                                            piece.dragging = True
                                            mx, my = transform(event.pos[0], event.pos[1], rotated)
                                            piece.offset = (piece.rect.x - mx, piece.rect.y - my)
                                            piece.origin = (piece.rect.x, piece.rect.y)
                                            valid_moves, occupied, castling_moves, en_passant_moves = get_legal_moves(piece, all_pieces, white_turn, turn_number)
                                            break
                
            #########################
            # Mouse button released #
            #########################
            elif event.type == pygame.MOUSEBUTTONUP:
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

                                # En passant capture
                                if piece.piece_type == "WP":
                                    origin_row = piece.origin[1] // 75
                                    if row == origin_row - 1 and col != piece.origin[0] // 75:
                                        # Diagonal move with no piece on destination = en passant
                                        if (col, row) not in {(p.rect.x // 75, p.rect.y // 75) for p in all_pieces if p != piece}:
                                            for target_piece in all_pieces[:]:
                                                if target_piece.rect.x // 75 == col and target_piece.rect.y // 75 == origin_row:
                                                    all_pieces.remove(target_piece)
                                                    break
                                elif piece.piece_type == "BP":
                                    origin_row = piece.origin[1] // 75
                                    if row == origin_row + 1 and col != piece.origin[0] // 75:
                                        # Diagonal move with no piece on destination = en passant
                                        if (col, row) not in {(p.rect.x // 75, p.rect.y // 75) for p in all_pieces if p != piece}:
                                            for target_piece in all_pieces[:]:
                                                if target_piece.rect.x // 75 == col and target_piece.rect.y // 75 == origin_row:
                                                    all_pieces.remove(target_piece)
                                                    break

                                piece.rect.x = col * 75
                                piece.rect.y = row * 75
                                piece.move_counter += 1

                                # Increments pawn movement for en passant validity
                                if piece.piece_type in ("WP", "BP"):
                                    origin_row = piece.origin[1] // 75
                                    if abs(row - origin_row) == 2:
                                        piece.last_double_advance_turn = turn_number

                                # Castling: if king moved 2 squares, move the rook too
                                if piece.piece_type in ("WK", "BK") and abs(col - (piece.origin[0] // 75)) == 2:
                                    if col == 6:  # Kingside
                                        rook_origin_col, rook_dest_col = 7, 5
                                    else:         # Queenside
                                        rook_origin_col, rook_dest_col = 0, 3
                                    for p in all_pieces:
                                        if p.rect.x // 75 == rook_origin_col and p.rect.y // 75 == row:
                                            p.rect.x = rook_dest_col * 75
                                            p.move_counter += 1
                                            break

                                turn_number += 1
                                time.sleep(0.75)
                                white_turn = not white_turn

                                in_check = is_in_check(all_pieces, white_turn)
                                if is_checkmate(all_pieces, white_turn, turn_number):
                                    game_over = True

                                rotated = not rotated
                            else:
                                piece.rect.x, piece.rect.y = piece.origin

                        piece.dragging = False
                    valid_moves = []
                    castling_moves = set()

            ###############
            # Mouse moves #
            ###############
            elif event.type == pygame.MOUSEMOTION:
                for piece in all_pieces:
                    if piece.dragging:
                        mx, my = transform(event.pos[0], event.pos[1], rotated)
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

        # Draw pieces: non-dragging first, then dragging on top.
        for piece in all_pieces:
            if not piece.dragging:
                dx, dy = transform(piece.rect.x, piece.rect.y, rotated)
                window.blit(piece.image, (dx, dy))

        for piece in all_pieces:
            if piece.dragging:
                dx, dy = transform(piece.rect.x, piece.rect.y, rotated)
                window.blit(piece.image, (dx, dy))

        # Highlights valid move location
        for (col, row) in valid_moves:
            dx, dy = transform(col * 75, row * 75, rotated)
            target = (col, row)
            highlight = pygame.Surface((75, 75), pygame.SRCALPHA)
    
            if target in en_passant_moves:
                highlight.fill((255, 128, 128, 128))
            elif target in occupied and occupied[target]:
                highlight.fill((255, 128, 128, 128))  # red - capture
            elif target in castling_moves:
                highlight.fill((100, 149, 237, 128))  # blue - castling
            else:
                highlight.fill((144, 238, 144, 128))  # green - normal move
            
            window.blit(highlight, (dx, dy))
        
        if promoting:
            options = ["WQ", "WR", "WB", "WN"] if promoting_piece.piece_type == "WP" else ["BQ", "BR", "BB", "BN"]
            for i, option in enumerate(options):
                pygame.draw.rect(window, GRAY, (i * 75, 262, 75, 75))
                window.blit(images[option], (i * 75, 262))

        if game_over:
            msg = "Checkmate! " + ("Black" if white_turn else "White") + " wins!"
            text = font.render(msg, True, (200, 0, 0))
            window.blit(text, (600 // 2 - text.get_width() // 2, 600 // 2 - text.get_height() // 2))
        elif in_check:
            msg = ("White" if white_turn else "Black") + " is in check!"
            text = font.render(msg, True, (200, 0, 0))
            window.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

main()