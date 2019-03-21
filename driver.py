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
import searchBiDir
import os
import glob

if __name__ == "__main__":
    counter = 0
    a_avg = 0
    b_avg = 0
    c_avg = 0
    d_avg = 0
    board_names = glob.glob("boards/*.blx")
    for board_name in board_names:
        print("Loading board file %s" % (board_name,))

        with open(board_name) as file:
            board = Board.read_board(file)
        bp0 = BloxorzProblem(board)

        searcher = searchGeneric.AStarSearcher(bp0)
        result = searcher.search()
        if result is None:
            print("For board %s, A Star Search found no solution!" % (board_name,))
            continue

        sequence = [arc.action for arc in result.arcs()]
        a = len(sequence)
        print("For board %s, A Star Search found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))

        searcher = searchBFS.BFSMultiPruneSearcher(bp0)
        result = searcher.search()
        if result is None:
            print("For board %s, BFS Multipath Pruning Search found no solution!" % (board_name,))
            continue

        sequence = [arc.action for arc in result.arcs()]
        b = len(sequence)
        print("For board %s, BFS Multipath Pruning Search found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))

        searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
        result = searcher.search()
        if result is None:
            print("For board %s, A Star Multipath Pruning Search found no solution!" % (board_name,))
            continue

        sequence = [arc.action for arc in result.arcs()]
        c = len(sequence)
        print("For board %s, A Star Multipath Pruning Search found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))

        searcher = searchBiDir.BidirectionalSeacher(bp0)
        result = searcher.search()
        if result is None:
            print("For board %s, Bidirectional Search found no solution!" % (board_name,))
            continue

        sequence = [arc.action for arc in result.arcs()]
        d = len(sequence)
        print("For board %s, Bidirectional Search found solution with length %d using %d forward expansions and %d backward expansions" % (board_name, len(sequence), searcher.num_expanded_forward, searcher.num_expanded_backward))

        assert a == b and b == c and c == d

    print(); print()






