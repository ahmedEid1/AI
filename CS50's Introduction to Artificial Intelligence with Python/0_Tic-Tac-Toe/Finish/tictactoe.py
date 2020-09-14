"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # x --> odd y --> even
    turns = 1

    for row in board:
        for cell in row:
            if cell is not None:
                turns += 1
    if turns % 2 == 0:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions_set = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                actions_set.add((i, j))

    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)

    if copy_board[action[0]][action[1]] is not None:
        raise Exception("not a valid action")

    turn = player(copy_board)

    copy_board[action[0]][action[1]] = turn

    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # horizontal
    for row in board:
        if all(cell == X for cell in row):
            return X
        if all(cell == O for cell in row):
            return O
    # vertical
    for i in range(3):
        if all(board[j][i] == X for j in range(3)):
            return X
        if all(board[j][i] == O for j in range(3)):
            return O
    # cross
    if all(board[i][i] == X for i in range(3)):
        return X
    if all(board[i][i] == O for i in range(3)):
        return O

    if all(board[i][abs(i-2)] == X for i in range(2, -1, -1)):
        return X

    if all(board[i][abs(i-2)] == O for i in range(2, -1, -1)):
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    full = 0
    for row in board:
        if any(cell is None for cell in row):
            break
        full += 1

    if full == 3:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    if win == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    turn = player(board)
    actions_set = actions(board)
    if turn == X:
        action = actions_set.pop()
        action_result = min_value(result(board, action))

        for a in actions_set:
            if min_value(result(board, a)) > action_result:
                action = a
        return action

    if turn == O:
        action = actions_set.pop()
        action_result = max_value(result(board, action))

        for a in actions_set:
            if max_value(result(board, a)) < action_result:
                action = a
        return action


def max_value(board):

    if terminal(board):
        return utility(board)

    v = float('-inf')

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):

    if terminal(board):
        return utility(board)

    v = float('inf')

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v



