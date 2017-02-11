#!/usr/bin/python3

import state
from state import *
import ui_ascii

def main():
    # Entry point
    board = Board({
        (0,0): Piece(ANT, 0),
        (-1,0): Piece(BEETLE, 1),
        (1,0): Piece(SPIDER, 0),
        (-1,1): Piece(GRASSHOPPER, 1),
        (2,1): Piece(QUEEN, 0),
    })
    ui = ui_ascii.UI(board)
    ui.print()

    # print('')
    # print('My pieces: ' + str(list(board.my_pieces())))
    # print('Opponent pieces: ' + str(list(board.opponent_pieces())))
    # print('Occupied neighours: ' + str(list(board.occupied_neighbours((0, 0)))))
    # print('Empty neighours: ' + str(list(board.empty_neighbours((0, 0)))))
    # print('My neighours: ' + str(list(board.my_neighbours((0, 0)))))
    # print('Opponent neighours: ' + str(list(board.opponent_neighbours((0, 0)))))
    # print('Connected placements: ' +str( board.connected_placements()))
    # print('New placements: ' + str(board.new_placements()))
    # print('Removable: ' + str(board.removable((0, 0))))
    # print('Removable: ' + str(board.removable((-1, 1))))


if __name__ == '__main__':
    main()

