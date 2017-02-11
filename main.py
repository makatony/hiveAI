#!/usr/bin/python3

import state
from state import Piece


# Entry point
board = state.Board({
    (0, 0): Piece(state.ANT, 0),
    (0, 1): Piece(state.ANT, 1)
})
print(board)
print('My pieces: ' + str(list(board.my_pieces())))
print('Opponent pieces: ' + str(list(board.opponent_pieces())))
print('Occupied neighours: ' + str(list(board.occupied_neighbours((0, 0)))))
print('Empty neighours: ' + str(list(board.empty_neighbours((0, 0)))))
print('My neighours: ' + str(list(board.my_neighbours((0, 0)))))
print('Opponent neighours: ' + str(list(board.opponent_neighbours((0, 0)))))
print('Connected placements: ' +str( board.connected_placements()))
print('New placements: ' + str(board.new_placements()))

