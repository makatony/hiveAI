# Piece type
ANT = "A"
BEETLE = "B"
GRASSHOPPER = "G"
QUEEN = "Q"
SPIDER = "S"

# Number of players
PLAYERS = 2


class Board:
    def __init__(self, positions = {}):
        """Create a new board with specified positions of the pieces"""
        # stack of available pieces: player number -> (insect -> count)
        self.stack = dict((player, { ANT: 3, BEETLE: 2, GRASSHOPPER: 3, QUEEN: 1, SPIDER: 2 }) for player in range(PLAYERS))

        # map of position: (x,y) -> Piece
        self.positions = positions
        for position, piece in positions.items():
            self.stack[piece.player][piece.insect] = max(self.stack[piece.player][piece.insect] - 1, 0)

        # next player number
        self.next_player = 0

#    def valid_moves(self, position):
#        return set()

    def valid_moves(self):
        """Yields tuple (insect, source_position, target_position) for each valid move."""
        # New placements.
        new_placements = list(self.new_placements())
        print(self.stack[self.next_player].items())
        for insect, count in self.stack[self.next_player].items():
            print(insect, count)
            if count > 0:
                for target_position in new_placements:
                    yield (insect, None, target_position)

        # TODO: moves.

    def removable(self, position):
        """Determine whether a piece on specified position is removable without splitting the hive."""
        start_neighbours = set(self.occupied_neighbours(position))
        if len(start_neighbours) < 2 or len(start_neighbours) > 4:
            return True
        visited = set()
        visited.add(position)
        remaining = set(list(start_neighbours)[:1])
        while remaining:
            new_remaining = set()
            for position in remaining:
                new_remaining.update(neighbour for neighbour in self.occupied_neighbours(position) if neighbour not in visited)
            visited.update(remaining)
            remaining = new_remaining
        return not start_neighbours - visited

    def new_placements(self):
        """Return tuple with valid placements for a new piece. These are connected placements not neighbouring any opponent's pieces."""
        # Trivial case: first piece in play:
        if len(self.positions) == 0:
            return ((0,0),)

        # Second trivial case: second piece in play:
        if len(self.positions) == 1:
            return self.neighbours((0,0))

        # Gather all empty spaces connected to friendly pieces.
        connected = set()
        for position, piece in self.positions.items():
            if piece.player == self.next_player:
                connected.update(self.empty_neighbours(position))

        # Filter them for 
        return tuple(position for position in connected if not list(self.opponent_neighbours(position)))

    def my_pieces(self):
        """Positions with next player's pieces"""
        return (position for position, piece in self.positions.items() if piece.player == self.next_player)

    def opponent_pieces(self):
        """Positions with opponent player's pieces"""
        return (position for position, piece in self.positions.items() if piece.player != self.next_player)

    def my_neighbours(self, position):
        """Neighbouring positions with next player's piece"""
        return (pos for pos in self.occupied_neighbours(position) if self.positions[pos].player == self.next_player)

    def opponent_neighbours(self, position):
        """Neighbouring positions with opponent's piece"""
        return (pos for pos in self.occupied_neighbours(position) if self.positions[pos].player != self.next_player)

    def occupied_neighbours(self, position):
        """Neighbouring positions with a piece"""
        return (pos for pos in self.neighbours(position) if pos in self.positions)

    def empty_neighbours(self, position):
        """Neighbouring positions without a piece"""
        return (pos for pos in self.neighbours(position) if pos not in self.positions)

    def neighbours(self, position):
        """Valid neighbouring positions"""
        (x, y) = position
        if x % 2 == 0:
            return [(x, y - 1), (x + 1, y - 1), (x + 1, y), (x, y + 1), (x - 1, y), (x - 1, y - 1)]
        else:
            return [(x, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]

    def __str__(self):
        return "not implemented"


class Piece:
    def  __init__(self, insect, player):
        # Insect
        self.insect = insect
    
        # Player number 
        self.player = player


