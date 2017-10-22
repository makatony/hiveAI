import random


class RandomAI:
    """Random BOT: it trivially plays a random move at every turn.
    """

    def __init__(self):
        pass

    def play(self, board):
        """Returns insect, src, tgt tuple."""
        valid_moves = [m for m in board.valid_moves()]
        if not valid_moves:
            return None
        return random.choice(valid_moves)
