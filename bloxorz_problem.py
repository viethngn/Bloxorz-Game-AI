##############################################################################
#
# File:         bloxorz_problem.py
# Date:         Wed 31 Aug 2011  11:40
# Author:       Ken Basye
# Description:  Bloxorz search problem
#
##############################################################################

import cs210_utils
from searchProblem import Arc, Search_problem
import searchGeneric
import searchBFS
#import searchBranchAndBound
import io
from bloxorz import Board, next_position

class BloxorzProblem(Search_problem):
    """
    >>> board_string = (
    ... '''BLOX 1
    ... 5 3
    ... X X X O O
    ... S X G X O
    ... W W W W X
    ... ''')
    
    >>> fake_file = io.StringIO(board_string)
    >>> board0 = Board.read_board(fake_file)
    >>> bp0 = BloxorzProblem(board0)
    >>> bp0.start
    ((0, 1), (0, 1))

    >>> searcher = searchBFS.BFSSearcher(bp0)
    >>> path = searcher.search()  #doctest: +SKIP
    2507 paths have been expanded and 2399 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))
    
    >>> a_pos, b_pos = path.end()   #doctest: +SKIP
    >>> a_pos == b_pos == board0.goal   #doctest: +SKIP
    True

    >>> searcher = searchBFS.BFSMultiPruneSearcher(bp0)
    >>> path = searcher.search()   #doctest: +SKIP
    16 paths have been expanded and 1 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> searcher = searchGeneric.AStarSearcher(bp0)
    >>> path = searcher.search()   #doctest: +SKIP
    1259 paths have been expanded and 1880 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))


    >>> bp0.heuristic = bp0.heuristic1  #doctest: +SKIP
    >>> searcher = searchGeneric.AStarSearcher(bp0)
    >>> path = searcher.search()   #doctest: +SKIP
    845 paths have been expanded and 1369 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> bp0.heuristic = bp0.heuristic1  #doctest: +SKIP
    >>> searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
    >>> path = searcher.search()   #doctest: +SKIP
    15 paths have been expanded and 1 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

"""
    def __init__(self, board):
        """
        Build a problem instance from a board
        """
        self.board = board
        self.start = (board.start, board.start)
        self.goal = (board.goal, board.goal)
        
    def start_node(self):
        """Returns start node"""
        return self.start
    
    def is_goal(self,node):
        """Returns True if node is a goal"""
        return node == self.goal

    def goal_node(self):
        """Returns start node"""
        return self.goal   
  
    def is_start(self,node):
        """Returns True if node is a goal"""
        return node == self.start         

    def neighbors(self,node,reverse_direction=False):
        """
        Given a node, return a sequence of Arcs usable
        from this node. 
        """
        #sequence of arcs
        seq = []
        #Actions
        ACTIONS = tuple(('U', 'D', 'L', 'R'))
        #Get next neighbor from current node position
        for item in ACTIONS:
          #print(item)
          neighbor = next_position(node, item, reverse_direction)

          #check if is a legal position on board
          if self.board.legal_position(neighbor):
            #Make arc
            arc = Arc(node, neighbor, 1, item)
            #print(neighbor)            
            seq.append(arc)
        #return
        return seq

    def heuristic(self, node):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        c = 1.5
        ((ax, ay), (bx, by)) = a_pos, b_pos = node
        (gx, gy) = self.board.goal
        da = abs(gx - ax) + abs(gy - ay)
        db = abs(gx - bx) + abs(gy - by)
        manhattan = max(da, db)
        return manhattan/c

if __name__ == '__main__':
    cs210_utils.cs210_mainstartup()

