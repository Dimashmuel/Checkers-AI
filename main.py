import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK, GREY
from checkers.game import Game
from minimax.algorithm import minimax
from MCTS.algorithm import mcts
import sys

# Game settings
FPS = 60
DEPTH = 4  # Depth for Minimax search
SIMULATIONS = 20  # Number of simulations for MCTS
AI_ALGORITHM = None  # Selected AI algorithm

# Initialize pygame and set up the display
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def draw_button(text, x, y, width, height, color, font_size):
    """
    Draws a button on the screen.
    - text: Button label
    - x, y: Button coordinates
    - width, height: Button dimensions
    - color: Button color
    - font_size: Size of the text font
    """
    pygame.draw.rect(WIN, color, (x, y, width, height))
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    WIN.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)


def display_winner(winner):
    """
    Displays the winner on the screen before closing the game.
    """
    WIN.fill(WHITE)
    font = pygame.font.Font(None, 70)
    if winner == WHITE:
        winner_text = f"Winner: {'User' if AI_ALGORITHM is None else 'AI (' + AI_ALGORITHM + ')'}"
    else:
        winner_text = "Winner: Opponent"
    text_surface = font.render(winner_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)  # Display for 3 seconds before closing


def choose_ai():
    """
    Displays AI selection menu and waits for user input.
    """
    global AI_ALGORITHM
    running = True

    while running:
        WIN.fill(WHITE)

        font = pygame.font.Font(None, 50)
        text_surface = font.render("Choose AI:", True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        WIN.blit(text_surface, text_rect)

        # Buttons for AI selection
        minimax_button = draw_button("Minimax", WIDTH // 4, HEIGHT // 2, 200, 60, GREY, 40)
        mcts_button = draw_button("MCTS", (WIDTH // 4) * 2, HEIGHT // 2, 200, 60, GREY, 40)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if minimax_button.collidepoint(event.pos):
                    AI_ALGORITHM = "Minimax"
                    running = False
                elif mcts_button.collidepoint(event.pos):
                    AI_ALGORITHM = "MCTS"
                    running = False


def get_row_col_from_mouse(pos):
    """
    Converts mouse position to board row and column.
    """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    """
    Main function to run the checkers game loop.
    """
    choose_ai()
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        # AI move execution
        if game.turn == WHITE:
            if AI_ALGORITHM == "Minimax":
                value, new_board = minimax(game.get_board(), DEPTH, True, game)
            elif AI_ALGORITHM == "MCTS":
                new_board = mcts(game.get_board(), SIMULATIONS, game)

            if new_board:
                game.ai_move(new_board)

        # Check for a winner
        if game.winner() is not None:
            display_winner(game.winner())  # Show the winner on screen before exiting
            run = False

        # Handle user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
