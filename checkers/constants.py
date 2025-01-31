import pygame

# Screen dimensions
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS  # Size of each square on the board

# RGB color definitions
BROWN = (139, 69, 19)  # Player one pieces
WHITE = (255, 255, 255)  # Player two pieces
BLACK = (0, 0, 0)  # Board background
BLUE = (0, 0, 255)  # Highlight color for valid moves
GREY = (128, 128, 128)  # Outline color for pieces

# Load and scale crown image for king pieces
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
