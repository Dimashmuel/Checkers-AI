import pygame
from .constants import ROWS, SQUARE_SIZE, COLS, WHITE, BLACK, BROWN
from .piece import Piece


class Board:
    def __init__(self):
        """
        Initializes the board, sets up pieces, and keeps track of remaining pieces.
        """
        self.board = []
        self.brown_left = self.white_left = 12  # Number of pieces per player
        self.brown_kings = self.white_kings = 0  # Number of kings per player
        self.create_board()

    def draw_squares(self, win):
        """
        Draws the checkerboard pattern on the game window.
        """
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        """
        Evaluates the board state. Positive values favor white, negative favor brown.
        """
        return self.white_left - self.brown_left + (self.white_kings * 0.5 - self.brown_kings * 0.5)

    def get_all_pieces(self, color):
        """
        Retrieves all pieces of a given color from the board.
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        """
        Moves a piece to a new position and promotes it if it reaches the opponent's back row.
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:  # Promote to king
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.brown_kings += 1

    def get_piece(self, row, col):
        """
        Returns the piece located at the given row and column.
        """
        return self.board[row][col]

    def create_board(self):
        """
        Initializes the board with pieces placed in starting positions.
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BROWN))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        """
        Draws the current board state, including all pieces.
        """
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        """
        Removes captured pieces from the board and updates piece count.
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BROWN:
                    self.brown_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        """
        Determines the winner of the game. Returns None if the game is ongoing.
        """
        if self.brown_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BROWN

        for color in [BROWN, WHITE]:
            for piece in self.get_all_pieces(color):
                if self.get_valid_moves(piece):
                    return None

        return "Draw"  # No valid moves for both players

    def get_valid_moves(self, piece):
        """
        Returns all valid moves for a given piece, including possible captures.
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BROWN or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """
        Helper function to check for valid left-side moves and captures.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    moves.update(self._traverse_left(r + step, stop, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, stop, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """
        Helper function to check for valid right-side moves and captures.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    moves.update(self._traverse_left(r + step, stop, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, stop, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves
