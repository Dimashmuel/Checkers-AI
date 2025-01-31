import pygame
from .constants import BROWN, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board


class Game:
    def __init__(self, win):
        """
        Initializes the game state, including the board and turn tracking.
        """
        self._init()
        self.win = win

    def update(self):
        """
        Updates the game display by redrawing the board and valid moves.
        """
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        """
        Resets the game state, initializing the board and setting the first turn.
        """
        self.selected = None
        self.board = Board()
        self.turn = BROWN  # Brown moves first
        self.valid_moves = {}

    def winner(self):
        """
        Checks if there is a winner in the current game state.
        """
        return self.board.winner()

    def reset(self):
        """
        Resets the game to the initial state.
        """
        self._init()

    def select(self, row, col):
        """
        Handles the selection of a piece and determines its valid moves.
        """
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)

            # Ensure multiple jump options are prioritized
            eating_moves = {pos: skips for pos, skips in self.valid_moves.items() if skips}
            if eating_moves:
                self.valid_moves = eating_moves
            return True

        return False

    def _move(self, row, col):
        """
        Moves the selected piece to the specified location and handles captures.
        """
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)

                # Check for additional jumps
                new_valid_moves = self.board.get_valid_moves(self.selected)
                eating_moves = {pos: skips for pos, skips in new_valid_moves.items() if skips}

                if eating_moves:
                    self.valid_moves = eating_moves
                    return True  # Allow the player to continue jumping
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        """
        Highlights valid moves on the game board.
        """
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        """
        Switches the active player and resets valid moves.
        """
        self.valid_moves = {}
        if self.turn == BROWN:
            self.turn = WHITE
        else:
            self.turn = BROWN

    def get_board(self):
        """
        Returns the current board state.
        """
        return self.board

    def ai_move(self, board):
        """
        Handles AI-controlled moves and changes turn afterward.
        """
        self.board = board
        self.change_turn()
