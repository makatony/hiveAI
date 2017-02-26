#!/usr/bin/python3

import unittest

from state import *
import ui_ascii


class TestState(unittest.TestCase):

    def _print_board(self, board):
        ui = ui_ascii.UI(board)
        ui.print()

    def _list_moves(self, board, insect, piece_pos):
        return sorted([move[2] for move in board.valid_moves() if move[0] == insect and move[1] == piece_pos])

    def test_removable(self):
        layout = {
            (0, 0): Piece(ANT, 0),
            (-1, 0): Piece(BEETLE, 1),
            (1, 0): Piece(SPIDER, 0),
            (-1, 1): Piece(QUEEN, 1),
            (2, 1): Piece(QUEEN, 0),
            (-1, 2): Piece(GRASSHOPPER, 1),
            (1, 1): Piece(SPIDER, 0),
            (-1, 3): Piece(SPIDER, 1),
        }
        removable = set([(-1, 3), (1, 1), (2, 1)])
        board = Board(layout)
        # self._print_board(board)
        for pos in layout.keys():
            if pos in removable:
                self.assertTrue(board.is_removable(pos), "position %s should be removable" % (pos,))
            else:
                self.assertFalse(board.is_removable(pos), "position %s should NOT be removable" % (pos,))

    def test_queen_moves(self):
        # Check it doesn't break the hive.
        layout = {
            (0, 0): Piece(ANT, 0),
            (-1, 0): Piece(BEETLE, 1),
            (1, 0): Piece(SPIDER, 0),
            (-1, 1): Piece(GRASSHOPPER, 1),
            (2, 1): Piece(QUEEN, 0),
            (-1, 2): Piece(GRASSHOPPER, 1),
        }
        board = Board(layout)
        queen_moves = self._list_moves(board, QUEEN, (2, 1))
        # self._print_board(board)
        self.assertEqual(queen_moves, [(1, 1), (2, 0)])

        # Now queen can't move because it would break hive.
        layout[(3, 1)] = Piece(GRASSHOPPER, 0)
        board = Board(layout)
        queen_moves = self._list_moves(board, QUEEN, (2, 1))
        self.assertFalse(queen_moves)

        # If we put some pieces around it can move again.
        layout[(1, 1)] = Piece(BEETLE, 0)
        layout[(2, 2)] = Piece(BEETLE, 0)
        board = Board(layout)
        queen_moves = self._list_moves(board, QUEEN, (2, 1))
        self.assertEqual(queen_moves, [(2, 0), (3, 0)])

        # Finally piece is not supposed to squeeze among pieces:
        layout[(2, 0)] = Piece(ANT, 0)
        board = Board(layout)
        queen_moves = self._list_moves(board, QUEEN, (2, 1))
        # self._print_board(board)
        self.assertFalse(queen_moves)

    def test_spider_moves(self):
        layout = {
            (0, 0): Piece(ANT, 0),
            (-1, 0): Piece(BEETLE, 1),
            (1, 0): Piece(SPIDER, 0),
            (-1, 1): Piece(QUEEN, 1),
            (2, 1): Piece(QUEEN, 0),
            (-1, 2): Piece(GRASSHOPPER, 1),
            (1, 1): Piece(SPIDER, 0),
            (-1, 3): Piece(SPIDER, 1),
        }
        board = Board(layout)

        # Spider at 1_0 should be locked in place (it would break the hive)
        spider_moves = self._list_moves(board, SPIDER, (1, 0))
        self.assertFalse(spider_moves)

        # Spider at (1,1)
        spider_moves = self._list_moves(board, SPIDER, (1, 1))
        self.assertEqual(spider_moves, [(0, 3), (0, 4), (3, 0)])

        # Other player spider, at -1,3
        board.next_player = 1
        spider_moves = self._list_moves(board, SPIDER, (-1, 3))
        self.assertEqual(spider_moves, [(-2, 1), (0, 2), (1, 2), (2, 2)])

    def test_grasshoper_moves(self):
        layout = {
            (0, 0): Piece(ANT, 0),
            (-1, 0): Piece(BEETLE, 1),
            (1, 0): Piece(QUEEN, 0),
            (-1, 1): Piece(QUEEN, 1),
            (2, 1): Piece(GRASSHOPPER, 0),
            (-1, 2): Piece(GRASSHOPPER, 1),
            (1, 1): Piece(GRASSHOPPER, 0),
            (-1, 3): Piece(GRASSHOPPER, 1),
        }
        board = Board(layout)
        # self._print_board(board)

        # Grasshoppers at (2,1) and (1,1) can jump to 2 directions.
        moves = self._list_moves(board, GRASSHOPPER, (1, 1))
        self.assertEqual(moves, [(1, -1), (3, 0)])
        moves = self._list_moves(board, GRASSHOPPER, (2, 1))
        self.assertEqual(moves, [(-1, -1), (0, 2)])

        # Second player grasshopper at (-1,3)
        board.next_player = 1
        moves = self._list_moves(board, GRASSHOPPER, (-1, 3))
        self.assertEqual(moves, [(-1, -1)])

        # Grasshopper at (-1,2) should be blocked.
        moves = self._list_moves(board, GRASSHOPPER, (-1, 2))
        self.assertFalse(moves)

    def test_ant_moves(self):
        layout = {
            (0, 0): Piece(ANT, 0),
            (-1, 0): Piece(BEETLE, 1),
            (1, 0): Piece(QUEEN, 0),
            (-1, 1): Piece(QUEEN, 1),
            (2, 1): Piece(ANT, 0),
            (-1, 2): Piece(ANT, 1),
            (1, 1): Piece(ANT, 0),
            (-1, 3): Piece(ANT, 1),
        }
        board = Board(layout)
        # self._print_board(board)

        # Ant at (1,1) can move anywhere connected to the hive.
        moves = self._list_moves(board, ANT, (1, 1))
        self.assertEqual(moves, [(-2, 0), (-2, 1), (-2, 2), (-2, 3), (-2, 4), (-1, -1), (-1, 4),
                                 (0, -1), (0, 1), (0, 2), (0, 3), (0, 4), (1, -1), (2, 0), (2, 2), (3, 0), (3, 1)])

        # Ant at (2,1) is can't squeeze between pieces into (0,1), but anywhere
        # connected to the hive should be fine.
        moves = self._list_moves(board, ANT, (2, 1))
        self.assertEqual(moves, [(-2, 0), (-2, 1), (-2, 2), (-2, 3), (-2, 4), (-1, -1), (-1, 4),
                                 (0, -1), (0, 2), (0, 3), (0, 4), (1, -1), (1, 2), (2, 0), (2, 2)])

        # Second player grasshopper at (-1,3)
        board.next_player = 1
        # self._print_board(board)
        moves = self._list_moves(board, ANT, (-1, 3))
        self.assertEqual(moves, [(-2, 0), (-2, 1), (-2, 2), (-2, 3), (-1, -1), (0, -1),
                                 (0, 2), (0, 3), (1, -1), (1, 2), (2, 0), (2, 2), (3, 0), (3, 1)])

        # Ant at (-1,2) should be blocked.
        moves = self._list_moves(board, ANT, (-1, 2))
        self.assertFalse(moves)

    def test_beetle_moves(self):
        layout = {
            (0, 0): Piece(BEETLE, 0),
            (0, -1): Piece(ANT, 1),
            (0, 1): Piece(SPIDER, 0),
            (1, -2): Piece(BEETLE, 1),
            (1, 0): Piece(BEETLE, 0),
            (1, -3): Piece(QUEEN, 1),
            (0, 2): Piece(QUEEN, 0),
            (2, -1): Piece(SPIDER, 1),
            (2, 0): Piece(ANT, 0),
        }
        covered = {
            (0, 0): [Piece(ANT, 0), Piece(BEETLE, 1)],
        }
        board = Board(layout, covered)
        # self._print_board(board)

        # Beetle on 1,0: shouldn't be able to move to (1,-1).
        moves = self._list_moves(board, BEETLE, (1, 0))
        self.assertEqual(moves, [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)])

        # Beetle on 0,0: can move to any neighboor position.
        moves = self._list_moves(board, BEETLE, (0, 0))
        self.assertEqual(moves, [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)])

        # Player's 1 beetle at (1,-2) is blocked since it would break the hive.
        board.next_player = 1
        # self._print_board(board)
        moves = self._list_moves(board, BEETLE, (1, -2))
        self.assertFalse(moves)

    def _is_piece(self, piece, insect, player):
        return piece.insect == insect and piece.player == player

    def test_move(self):
        layout = {
            (0, 0): Piece(BEETLE, 0),
            (0, -1): Piece(ANT, 1),
            (0, 1): Piece(SPIDER, 0),
            (1, -2): Piece(BEETLE, 1),
            (1, 0): Piece(BEETLE, 0),
            (1, -3): Piece(QUEEN, 1),
            (0, 2): Piece(QUEEN, 0),
            (2, -1): Piece(SPIDER, 1),
            (2, 0): Piece(ANT, 0),
        }
        covered = {
            (0, 0): [Piece(ANT, 0), Piece(BEETLE, 1)],
        }
        board = Board(layout, covered)
        board.check_moves = True
        self._print_board(board)

        # Player 0: ynstack beetle.
        board.move(BEETLE, (0, 0), (1, -1))
        self.assertTrue(self._is_piece(board.positions[(1, 0)], BEETLE, 0))
        self.assertTrue((0, 0) in board.covered)
        self.assertEqual(len(board.covered[(0, 0)]), 1)
        self.assertTrue(self._is_piece(board.covered[(0, 0)][0], ANT, 0))
        self.assertTrue(self._is_piece(board.positions[(0, 0)], BEETLE, 1))

        # Player 1: move beetle.
        board.move(BEETLE, (0, 0), (-1, 0))
        self.assertTrue(self._is_piece(board.positions[(-1, 0)], BEETLE, 1))
        self.assertTrue((0, 0) not in board.covered)
        self.assertTrue(self._is_piece(board.positions[(0, 0)], ANT, 0))

        # Player 0: move ant and make sure board is left emtpy.
        board.move(ANT, (2, 0), (1, -4))
        self.assertTrue(self._is_piece(board.positions[(1, -4)], ANT, 0))
        self.assertTrue((2, 0) not in board.positions)

        # Player 1: put new piece into game.
        board.move(ANT, None, (3, -2))
        self.assertTrue(self._is_piece(board.positions[(3, -2)], ANT, 1))

        # Try placing a piece.


if __name__ == '__main__':
    unittest.main()
