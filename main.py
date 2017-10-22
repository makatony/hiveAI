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
    flags_parser.add_argument('--ai_ui', action='store_true')
    flags = flags_parser.parse_args()
    player_types = [flags.p0, flags.p1]

    # Initialize AIs
    ais = [create_ai(player_types[p]) for p in [0, 1]]

    # TODO: check end of game.
    board = Board()
    while True:
        # Check for end-of-game.
        end_of_game, winner = board.end_of_game()
        if end_of_game:
            ui = ui_ascii.UI(board, list_moves=False)
            ui.print()
            if winner == -1:
                print('\nDRAW!!!\n')
            else:
                print('\nPLAYER {} WINS'.format(winner))
            break

        player = board.next_player
        if player_types[player] == 'hotseat':
            ui = ui_ascii.UI(board)
            ui.print()

            valid = next(board.valid_moves(), None)
            if valid is None:
                _ = input('No valid move, press enter to continue')
                move = None
            else:
                move = ui.read()
            board.move(move)

        elif player_types[player] == 'ai':
            if flags.ai_ui:
                ui = ui_ascii.UI(board)
                ui.print()
            move = ais[player].play(board)
            if flags.ai_ui:
                print("Selected move: {}".format(move))

            board.move(move)

        else:
            raise ValueError('player of type \"{}\" not implemented'.format(player_types[player]))


def create_ai(player_type):
    """Creates AI player."""
    if player_type != 'ai':
        return None
    return RandomAI()

if __name__ == '__main__':
    main()
