import pygame
from .constants import SQUARE_SIZE, GREY, CROWN


class Piece:
    PADDING = 15  # Padding around the piece within the square
    OUTLINE = 2  # Outline thickness for the piece

    def __init__(self, row, col, color):
        """
        Initializes a piece with its row, column, and color.
        Also calculates its initial position on the board.
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False  # Indicates if the piece has been promoted to a king
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        """
        Calculates the center position of the piece on the board.
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """
        Promotes the piece to a king, allowing it to move both forward and backward.
        """
        self.king = True

    def draw(self, win):
        """
        Draws the piece on the board.
        If the piece is a king, a crown is displayed.
        """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)  # Draw outer outline
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)  # Draw main piece
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        """
        Moves the piece to a new row and column, then recalculates its position.
        """
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        """
        Returns a string representation of the piece (useful for debugging).
        """
        return f"{'King' if self.king else 'Piece'}({self.color})"
