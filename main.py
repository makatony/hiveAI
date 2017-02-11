#!/usr/bin/python3

import state
from state import Piece


# Entry point
board = state.Board({ (0, 0): Piece(state.ANT, 0) })
print(board)
print(list(board.my_neighbours((0, 0))))

