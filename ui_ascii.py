# Ascii UI, optionally colored
import math
import re

from state import *

class UI:
    """Ascii UI, can be used for printing, etc."""
    def __init__(self, board, color=True):
        self.board = board
        self.color = color
        self.min_x = min(x for x,_ in self.board.positions)
        self.max_x = max(x for x,_ in self.board.positions)
        self.min_y = min(y for _,y in self.board.positions)
        self.max_y = max(y for _,y in self.board.positions)

        # Index board's valid moves.
        moves = {}
        for move in self.board.valid_moves():
            key = (move[0], move[1])
            if not key in moves:
                moves[key] = [move[2]]
            else:
                moves[key] += [move[2]]
        self.moves = sorted(moves.items())

    # Each position in the board are represent by so many lines and chars.
    LINES_PER_ROW = 4
    CHARS_PER_COLUMN = 9

    # Command line input parsing.
    piece_move_re = re.compile('(\d+)\s+\(?(\-?\d+)\s*,\s*(\-?\d+)\)?\s*')
    piece_only_re = re.compile('(\d+)\s*')

    def print(self):
        for line in self._all_lines():
            print(line)

    def read(self):
        """Reads and parses next user move, returns (insect, src_pos, tgt_pos)."""
        while True:
            raw = input('Please enter your move: ')
            match = UI.piece_move_re.fullmatch(raw)
            if match is not None:
                ii = int(match.group(1))
                if ii < 0 or ii > len(self.moves):
                    print('Invalid piece #%d' % ii)
                    continue
                move_to = (int(match.group(2)), int(match.group(3)))
                if move_to not in self.moves[ii][1]:
                    print('Move to %s not valid' % (move_to,))
                    continue
                return (self.moves[ii][0][0], self.moves[ii][0][1], move_to)

            match = UI.piece_only_re.fullmatch(raw)
            if match is None:
                print('Unknown entry "%s"' % raw)
                continue
            ii = int(match.group(1))
            if ii < 0 or ii >= len(self.moves):
                print('Invalid piece #%d' % ii)
                continue
            if len(self.moves[ii][1]) > 1:
                print('Piece #%d have multiple target locations, you must specify' % ii)
                continue
            return (self.moves[ii][0][0], self.moves[ii][0][1], move_to)



    def _all_lines(self):
        for line in self._board_lines():
            yield line
        yield ''
        for line in self._stack_lines():
            yield line
        yield ''
        yield self._player_turn_line()
        for line in self._player_moves_lines():
            yield line


    def _stack_lines(self):
        """Yields lines representing pieces available in stack."""
        for (player, pieces) in self.board.stack.items():
            pieces_str_list = ["%s-%d" % (insect, count) for insect, count in sorted(pieces.items())]
            yield 'Player %d stack: %s' % (player, ', '.join(pieces_str_list))

    def _player_turn_line(self):
        piece = Piece(QUEEN, self.board.next_player)
        return '%sPlayer %d turn to play:%s' % (self._color_start(piece), self.board.next_player, self._color_end())

    def _player_moves_lines(self):
        example = None
        for ii in range(len(self.moves)):
            src = self.moves[ii][0][0]
            if self.moves[ii][0][1] is not None:
                src = 'move %s from %s to ' % (src, self.moves[ii][0][1])
            else:
                src = 'place new %s in ' % src
            if example is None:
                move_to = self.moves[ii][1][0]
                example = '  Example: to %s%s, type "%d %d,%d"' % (
                    src, move_to, ii, move_to[0], move_to[1])
            yield '  [%d] %s%s' % (ii, src, self.moves[ii][1])
        yield example
        yield '  (Note: if there is only one valid move for a piece, you can enter only the first number)'


    def _board_lines(self):
        """Yields lines of the printed board."""
        lines = []
        for line_y in range(UI.LINES_PER_ROW * (self.max_y - self.min_y + 1) + math.floor(UI.LINES_PER_ROW/2)):
            yield self._board_line(line_y)

    def _board_line(self, line_y):
        """Yields one line of the printed board: relative to self.min_y."""
        strips = []
        if self.min_y % 2 == 1:
            line_y -= math.floor(UI.LINES_PER_ROW/2)
        for x in range(self.min_x, self.max_x+2):
            adj_line_y = line_y
            if x % 2 == 1: 
                adj_line_y = line_y - math.floor(UI.LINES_PER_ROW/2)
            y = math.floor(adj_line_y/UI.LINES_PER_ROW)
            piece = None            
            if (x,y) in self.board.positions:
                piece = self.board.positions[(x,y)]
            sub_y = adj_line_y % UI.LINES_PER_ROW
            strips += [self._board_strip(piece, x, y, sub_y, is_final=(x==self.max_x+1))]
        return ''.join(strips)

    def _board_strip(self, piece, x, y, sub_y, is_final):
        """Yields a strip related to the given x column of a line of the board."""
        if sub_y == 0:
            if is_final: return ' /'
            return ' /'+(UI.CHARS_PER_COLUMN-2)*' '
        elif sub_y == 1:
            if is_final: return '/'
            coord = "%d,%d" % (x,y)
            return ('/ {:^' + str(UI.CHARS_PER_COLUMN-2) + '}').format(coord)
        elif sub_y == 2:
            if is_final: return '\\'
            if piece is None:
                return '\\ '+(UI.CHARS_PER_COLUMN-2)*' '
            else:
                if is_final: return ' \\'
                return ('\\ {:}{:^'+str(UI.CHARS_PER_COLUMN-2)+'}{:}').format(self._color_start(piece),piece.insect,self._color_end())                
        else:
            return ' \\'+(UI.CHARS_PER_COLUMN-2)*'_'

    def _color_start(self, piece):
        """Sets the color of a piece."""
        if not self.color:
            return ''
        if piece.player == 0:
            if piece.insect == QUEEN:
                return '\033[37;41;1m'
            else:
                return '\033[30;41;1m'
        else:
            if piece.insect == QUEEN:
                return '\033[37;42;1m'
            else:
                return '\033[30;42;1m'

    def _color_end(self):
        if not self.color:
            return ''
        return '\033[39;49;0m'