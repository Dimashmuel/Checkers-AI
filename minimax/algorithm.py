from copy import deepcopy
import pygame
from checkers.constants import BROWN, WHITE


def minimax(position, depth, max_player, game):
    """
    Implements the Minimax algorithm for decision-making in the game.
    - position: The current board state.
    - depth: The depth to search in the game tree.
    - max_player: Boolean flag indicating if it's the maximizing player's turn.
    - game: The game instance for additional context.
    """
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = sorted(get_all_moves(position, WHITE, game), key=lambda board: board.evaluate(), reverse=True)

        for move in moves:
            evaluation, _ = minimax(move, depth - 1, False, game)
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        moves = sorted(get_all_moves(position, BROWN, game), key=lambda board: board.evaluate())

        for move in moves:
            evaluation, _ = minimax(move, depth - 1, True, game)
            if evaluation < minEval:
                minEval = evaluation
                best_move = move

        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    """
    Simulates a move on the board without modifying the original state.
    Handles capturing mechanics if applicable.
    """
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
        new_valid_moves = board.get_valid_moves(piece)
        if any(new_valid_moves.values()):
            return simulate_chain_eating(piece, board, game, new_valid_moves)
    return board


def simulate_chain_eating(piece, board, game, valid_moves):
    """
    Recursively executes multiple captures if available.
    """
    for move, skip in valid_moves.items():
        if skip:
            board.move(piece, move[0], move[1])
            board.remove(skip)
            new_valid_moves = board.get_valid_moves(piece)
            if any(new_valid_moves.values()):
                return simulate_chain_eating(piece, board, game, new_valid_moves)
    return board


def get_all_moves(board, color, game):
    """
    Generates all possible moves for a given player color.
    Returns a list of board states after executing each move.
    """
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            if skip:
                moves.insert(0, new_board)  # Prioritize capturing moves
            else:
                moves.append(new_board)
    return moves


def draw_moves(game, board, piece):
    """
    Highlights valid moves on the board for the selected piece.
    """
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
