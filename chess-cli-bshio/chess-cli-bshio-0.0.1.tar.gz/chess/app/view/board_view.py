"""
Module for board related views.
"""
from chess.board import Position


def display(board):
    """ Displays board to standard out.

    Parameters
    ----------
    board : chess.board.Board
        Board to display

    Returns
    -------
    None
    """
    board_str = ''
    for rank in range(8, 0, -1):
        board_str += _generate_rank_line()
        board_str += _build_rank_str(board, rank)

    board_str += _generate_rank_line()
    board_str += '     a     b     c     d    e     f     g     h'
    print(board_str)


def _build_rank_str(board, rank):
    """ Builds string for a given rank (row).

    Parameters
    ----------
    board : chess.board.Board
        Board to display
    rank : int
        Rank to build string for.

    Returns
    -------
    str
        row representation for a given rank.
    """
    rank_str = '%s |' % rank
    for file in range(ord('a'), ord('h') + 1):
        position = Position('%s%s' % (chr(file), rank))
        piece = board.get_piece(position)
        if piece is None:
            rank_str += '     '
        else:
            rank_str += '{:^5}'.format(piece.symbol)

        rank_str += '|'

    rank_str += '\n'

    return rank_str


def _generate_rank_line():
    return '  -------------------------------------------------\n'
