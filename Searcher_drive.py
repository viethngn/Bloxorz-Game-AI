##############################################################################
#
# File:         driver.py
# Date:         Tue 11 Sep 2018  11:33
# Author:       Ken Basye
# Description:  Driver for testing bloxorz algorithms
#
##############################################################################

"""
Driver for testing bloxorz algorithms

"""

from bloxorz_problem import BloxorzProblem
from bloxorz import Board
import searchGeneric
import searchBFS
import os
import glob

if __name__ == "__main__":
    #board_names = glob.glob("boards/*.blx")
    board_names = glob.glob("boards/simple.blx")
    for board_name in board_names:
        print("Loading board file %s" % (board_name,))
        with open(board_name) as file:
            board = Board.read_board(file)
        bp0 = BloxorzProblem(board)
        searcher = searchGeneric.Searcher(bp0)
        result = searcher.search()
        if result is None:
            print("For board %s, found no solution!" % (board_name,))
            continue

        sequence = [arc.action for arc in result.arcs()]
        print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))

    print(); print()






