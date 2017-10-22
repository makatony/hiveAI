#!/usr/bin/python3

import argparse

from state import *
import ui_ascii
from random_ai import RandomAI


def main():
    # Entry point
    flags_parser = argparse.ArgumentParser(description='Play hive: hotseat, online, browser against AI, etc.')
    flags_parser.add_argument('--p0', action='store', default='hotseat', choices=['hotseat', 'online', 'ai'], dest='p0')
    flags_parser.add_argument('--p1', action='store', default='hotseat', choices=['hotseat', 'online', 'ai'], dest='p1')
    flags = flags_parser.parse_args()
    player_types = [flags.p0, flags.p1]

    # Initialize AIs
    ais = [create_ai(player_types[p]) for p in [0, 1]]

    # TODO: check end of game.
    board = Board()
    while True:
        player = board.next_player
        if player_types[player] == 'hotseat':
            ui = ui_ascii.UI(board)
            ui.print()
            insect, src, tgt = ui.read()
            board.move(insect, src, tgt)
        elif player_types[player] == 'ai':
            insect, src, tgt = ais[player].play(board)
            board.move(insect, src, tgt)
        else:
            raise ValueError('player of type \"{}\" not implemented'.format(player_types[player]))

    # {
    #     (0,0): Piece(ANT, 0),
    #     (-1,0): Piece(BEETLE, 1),
    #     (1,0): Piece(SPIDER, 0),
    #     (-1,1): Piece(GRASSHOPPER, 1),
    #     (2,1): Piece(QUEEN, 0),
    #     (-1,2): Piece(GRASSHOPPER, 1),
    # })
    # board.next_player=0
    # ui = ui_ascii.UI(board)
    # ui.print()
    # print(ui.read())

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


def create_ai(player_type):
    """Creates AI player."""
    if player_type != 'ai':
        return None
    return RandomAI()

if __name__ == '__main__':
    main()
