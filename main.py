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

if __name__ == '__main__':
    main()

