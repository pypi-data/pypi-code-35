"""
Module for two player game of chess.
"""
from chess.board import Board
from chess.board import IllegalMoveError
from chess.board import Position
from chess.app.view import board_view


QUIT = 'Q'


def play_game():
    """Play two player game of chess.

    Returns
    -------
    None
    """
    board = Board()
    quit_game = False
    while not quit_game:
        print('')
        display_board(board)

        while True:
            try:
                print('')
                user_input = ask_move()

                if user_input.upper() == QUIT:
                    quit_game = True
                    break

                position_from, position_to = _parse_positions(user_input)
                board.move_piece(position_from, position_to)
                break
            except ValueError as err:
                print(err)
            except IllegalMoveError as err:
                print(err)


def _parse_positions(user_input):
    positions = user_input.split()

    if len(positions) != 2:
        raise ValueError('Invalid move, needs two positions')

    position_from = Position(positions[0])
    position_to = Position(positions[1])

    return position_from, position_to


def display_board(board):
    """Displays current chess board state

    Parameters
    ----------
    board : chess.board.Board
        Board to display.

    Returns
    -------
    None
    """
    return board_view.display(board)


def ask_move():
    """Ask user for move to make.

    Returns
    -------
    str
        User movement input.
    """
    user_input = input('Make a move(ex. b2 b3) or Q to quit: ')
    return user_input


def move_piece(positionFrom, positionTo):
    """
    Move piece from one position to another on the board, possibly capturing an
    opponents piece.

    Parameters
    ----------
    positionFrom : Position
        Position to move piece from.
    positionTo : Position
        Position to move piece to.

    Returns
    -------
    None
    """
    raise NotImplementedError()


def capture_piece(position):
    """
    Capture piece if one is at given position.

    Parameters
    ----------
    position : Position

    Returns
    -------
    None
    """
    raise NotImplementedError()
