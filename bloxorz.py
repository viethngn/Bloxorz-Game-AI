##############################################################################
#
# File:         bloxorz.py
# Date:         Wed 31 Aug 2011  11:40
# Author:       Ken Basye
# Description:  Bloxorz utilities 
#
##############################################################################


"""
Classes and functions for the Bloxorz project

"""
import io
import cs210_utils
import sys
import types


class Board(object):
    """
    Simple representation of a Bloxorz board.  

    """

    def __init__(self, rows):
        """
        Construction is done with a sequence of sequences; they must all be the
        same length.
        
        >>> rows = (('S', 'X', 'O'), ('G', 'X', 'X'))
        >>> b0 = Board(rows)
        >>> b0.x_dim
        3
        >>> b0.y_dim
        2
        >>> b0.goal
        (0, 1)
        >>> b0.start
        (0, 0)

        Error checks:

        >>> rows = (('S', 'X'), ('G', 'Q'))
        >>> b1 = Board(rows)
        Traceback (most recent call last):
        ...
        ValueError: expected tile in ('S', 'X', 'G', 'W', 'O'), got Q

        """
        valid_board_chars = ('S', 'X', 'G', 'W', 'O')
        y_dim = len(rows)
        assert y_dim != 0, str(y_dim)
        x_dim = len(rows[0])
        assert x_dim != 0, str(x_dim)
        self.rows = list()
        start_count = goal_count = 0
        for y, row in enumerate(rows):
            assert len(row) == x_dim, str((x_dim, len(row)))
            for x, tile in enumerate(row):
                if tile not in valid_board_chars:
                    raise ValueError('expected tile in %s, got %s' % (valid_board_chars, tile))
                if tile == 'G':
                    goal_count += 1
                    self.goal = x, y
                elif tile == 'S':
                    start_count += 1
                    self.start = x, y
            self.rows.append(tuple(row))
        self.x_dim, self.y_dim = x + 1, y + 1
        if goal_count != 1:
            raise ValueError('expected exactly one goal tile')
        if start_count != 1:
            raise ValueError('expected exactly one start tile')


    def on_board(self, square):
        """
        Determine if *square* (x, y) is on the board, which means also not on a
        void position.
        
        """
        x, y = square
        return x >= 0 and  y >= 0 and x < self.x_dim and y < self.y_dim and self.rows[y][x] != 'O'


    def legal_position(self, pos):
        """
        Determine whether *pos* is a legal position on this board.
        A position is a pair of pairs.

        >>> board_string = (
        ... '''BLOX 1
        ... 5 3
        ... X X X O O
        ... S X G X O
        ... W W W W X
        ... ''')
        
        >>> fake_file = io.StringIO(board_string)
        >>> board0 = Board.read_board(fake_file)
        >>> sol0 = ('R', 'U', 'L', 'D', 'R', 'R', 'U', 'L', 'D', 'R')

        >>> pos = (board0.start, board0.start)
        >>> results = list()
        >>> for action in sol0:   #doctest: +SKIP
        ...     new_pos = next_position(pos, action)
        ...     legal = board0.legal_position(new_pos)
        ...     results.append(legal)
        ...     pos = new_pos

        >>> all(results)
        True

        """
        # Unpacking like this will also check that pos has the right structure
        ((ax, ay), (bx, by)) = a_pos, b_pos = pos
        # Off board 
        if not (self.on_board(a_pos) and self.on_board(b_pos)): return False

        # Upright on weak square
        if (ax, ay) == (bx, by) and self.rows[ay][ax] == 'W': return False

        return True

    HEADER_STRING = 'BLOX'
    CURRENT_VERSION = '1'
    SUPPORTED_VERSIONS = (CURRENT_VERSION,)
    @staticmethod
    def read_board(file):
        r"""
        Read a board from a file.  The format is show below; whitespace is used to separate tokens.
        Note that the first line in the file must be a header line with a supported version number.

        >>> board_string = (
        ... '''BLOX 1
        ... 5 3
        ... X X X O O
        ... S X G X O
        ... W W W W X
        ... ''')

        >>> fake_file = io.StringIO(board_string)
        >>> board0 = Board.read_board(fake_file)
        >>> board0.goal
        (2, 1)

        >>> board0.start
        (0, 1)

        """
        
        header_info = file.readline().split()
        if len(header_info) != 2 or header_info[0] != Board.HEADER_STRING or header_info[1] not in Board.SUPPORTED_VERSIONS:
            raise ValueError("expected valid board file header, but got %s" % (header_info,))
        
        dimensions = file.readline().split()
        if len(dimensions) != 2:
            raise ValueError("expected 2 board dimensions, but got %s" % (dimensions,))
        # This conversion will raise an error if either string cannot be converted to an int
        x_dim, y_dim = int(dimensions[0]), int(dimensions[1])
        if x_dim <= 0 or y_dim <= 0:
            raise ValueError("expected positive board dimensions, but got %s" % ((x_dim, y_dim),))
            
        rows = list()
        for row_idx, line in enumerate(file):
            tiles = line.split()
            if len(tiles) != x_dim:
                raise ValueError("expected row with %d tiles, but got %s in row %d" % (x_dim, tiles, row_idx))
            rows.append(tiles)
        if row_idx != y_dim - 1:
            raise ValueError("expected %d rows but got %d" % (y_dim, row_idx))
        return Board(rows)
    # End class Board

ACTIONS = tuple(('U', 'D', 'L', 'R'))

reverse_action_dict = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}

def next_position(pos, action, reverse_direction=False):
    """
    Given a position *pos* for the 1x2 block in the form of a pair of pairs and
    and *action* from the set of legal actions, return the resulting position.

    >>> up0 = ((0, 0), (0, 0))
    >>> [(action, next_position(up0, action)) for action in ACTIONS]  
    [('U', ((0, -2), (0, -1))), ('D', ((0, 1), (0, 2))), ('L', ((-2, 0), (-1, 0))), ('R', ((1, 0), (2, 0)))]

    >>> vert0 = ((0, 0), (0, 1))
    >>> [(action, next_position(vert0, action)) for action in ACTIONS]  #doctest: +SKIP
    [('U', ((0, -1), (0, -1))), ('D', ((0, 2), (0, 2))), ('L', ((-1, 0), (-1, 1))), ('R', ((1, 0), (1, 1)))]

    >>> horiz0 = ((0, 0), (1, 0))
    >>> [(action, next_position(horiz0, action)) for action in ACTIONS]  #doctest: +SKIP
    [('U', ((0, -1), (1, -1))), ('D', ((0, 1), (1, 1))), ('L', ((-1, 0), (-1, 0))), ('R', ((2, 0), (2, 0)))]

    >>> horiz1 = ((1, 1), (2, 1))
    >>> [(action, next_position(horiz1, action)) for action in ACTIONS]  #doctest: +SKIP
    [('U', ((1, 0), (2, 0))), ('D', ((1, 2), (2, 2))), ('L', ((0, 1), (0, 1))), ('R', ((3, 1), (3, 1)))]

    >>> horiz1 = ((1, 1), (2, 1))
    >>> [(action, next_position(horiz1, action, True)) for action in ACTIONS]  #doctest: +SKIP
    [('U', ((1, 2), (2, 2))), ('D', ((1, 0), (2, 0))), ('L', ((3, 1), (3, 1))), ('R', ((0, 1), (0, 1)))]

    """
    # Note, if we want to allow blocks to split up, we will have to rework this
    # function completely

    # Unpacking like this will also check that pos has the right structure
    ((ax, ay), (bx, by)) = a_pos, b_pos = pos

    if reverse_direction:
        action = reverse_action_dict[action]

    if action == 'U':
        if ax == bx and ay == by:
            ay -= 2
            by -= 1
            pos = ((ax, ay), (bx, by))
            return pos
        elif ax == bx:
            ay -= 1
            by -= 2
            pos = ((ax, ay), (bx, by))
            return pos
        else:
            ay -= 1
            by -= 1
            pos = ((ax, ay), (bx, by))
            return pos
    elif action == 'D':
        if ax == bx and ay == by:
            ay += 1
            by += 2
            pos = ((ax, ay), (bx, by))
            return pos
        elif ax == bx:
            ay += 2
            by += 1
            pos = ((ax, ay), (bx, by))
            return pos
        else:
            ay += 1
            by += 1
            pos = ((ax, ay), (bx, by))
            return pos
    elif action == 'L':
        if ax == bx and ay == by:
            ax -= 2
            bx -= 1
            pos = ((ax, ay), (bx, by))
            return pos
        elif ay == by:
            ax -= 1
            bx -= 2
            pos = ((ax, ay), (bx, by))
            return pos
        else:
            ax -= 1
            bx -= 1
            pos = ((ax, ay), (bx, by))
            return pos
    elif action == 'R':
        if ax == bx and ay == by:
            ax += 1
            bx += 2
            pos = ((ax, ay), (bx, by))
            return pos
        elif ay == by:
            ax += 2
            bx += 1
            pos = ((ax, ay), (bx, by))
            return pos
        else:
            ax += 1
            bx += 1
            pos = ((ax, ay), (bx, by))
            return pos
    else:
        return "Invalid command!"

if __name__ == '__main__':
    cs210_utils.cs210_mainstartup()





