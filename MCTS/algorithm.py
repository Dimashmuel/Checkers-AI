from copy import deepcopy
import random
from minimax.algorithm import get_all_moves
from checkers.constants import BROWN, WHITE


class Node:
    """
    Represents a node in the Monte Carlo Tree Search (MCTS) tree.
    Each node stores a board state, its parent, children, visit count, and value.
    """

    def __init__(self, board, parent=None):
        self.board = board  # The game board state at this node
        self.parent = parent  # Parent node in the tree
        self.children = []  # List of child nodes
        self.visits = 0  # Number of times this node was visited
        self.value = 0  # Cumulative value of the node

    def is_fully_expanded(self):
        """
        Checks if all possible moves have been expanded from this node.
        """
        return len(self.children) == len(get_all_moves(self.board, WHITE, None))

    def best_child(self):
        """
        Returns the best child node based on the highest value-to-visit ratio.
        """
        return max(self.children, key=lambda child: child.value / (child.visits + 1e-6))

    def expand(self):
        """
        Expands the node by adding a new child node for an unexplored move.
        """
        moves = get_all_moves(self.board, WHITE, None)
        for move in moves:
            if not any(child.board == move for child in self.children):
                child_node = Node(move, self)
                self.children.append(child_node)
                return child_node
        return None


def mcts(board, iterations, game):
    """
    Performs Monte Carlo Tree Search (MCTS) to determine the best move.
    - board: The current game board state.
    - iterations: Number of simulations to run.
    - game: Game instance for additional context.
    """
    root = Node(deepcopy(board))

    for _ in range(iterations):
        node = root

        # Selection: Navigate the tree to find the best child
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # Expansion: Expand the tree by adding a new node
        new_node = node.expand()
        if new_node is None:
            continue

        # Simulation: Perform a random playout to determine the outcome
        winner = simulate_random_playout(new_node.board)

        # Backpropagation: Update the tree with the simulation results
        backpropagate(new_node, winner)

    return root.best_child().board


def simulate_random_playout(board):
    """
    Simulates a random game from the given board state until a winner is determined.
    """
    temp_board = deepcopy(board)
    while temp_board.winner() is None:
        moves = get_all_moves(temp_board, WHITE, None)
        if not moves:
            break
        temp_board = random.choice(moves)  # Select a random move
    return temp_board.winner()


def backpropagate(node, winner):
    """
    Updates the values and visit counts of nodes in the MCTS tree based on the simulation outcome.
    """
    while node:
        node.visits += 1
        if winner == WHITE:
            node.value += 1  # Reward for a win
        elif winner == BROWN:
            node.value -= 1  # Penalty for a loss
        node = node.parent
