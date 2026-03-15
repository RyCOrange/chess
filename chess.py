import pygame

# Define colors (RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
FPS = 30

class piece:
    def __init__(self, name, moves):
        piece.name = name
        piece.moves = moves

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

    piece_image = pygame.image.load("wp.png").convert_alpha()
    piece_image = pygame.transform.scale(piece_image, (75, 75))  # Scale to square size

    object_rect = pygame.Rect(100, 100, 75, 75)
    is_dragging = False
    offset = (0, 0)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if object_rect.collidepoint(event.pos):
                        is_dragging = True
                        mouse_x, mouse_y = event.pos
                        offset = (object_rect.x - mouse_x, object_rect.y - mouse_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    mouse_x, mouse_y = event.pos
                    object_rect.x = mouse_x + offset[0]
                    object_rect.y = mouse_y + offset[1]

        # Redraw board
        window.fill(WHITE)
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(window, BLACK, (col * 75, row * 75, 75, 75))

        # Draw sprite
        window.blit(piece_image, object_rect)

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

main()