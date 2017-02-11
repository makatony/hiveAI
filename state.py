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
        for (position, piece) in positions.items():
            self.stack[piece.player][piece.insect] = max(self.stack[piece.player][piece.insect] - 1, 0)

        # next player number
        self.next_player = 0

    def connected_placements(self):
        """Connected placements for an already connected piece. These are positions connected to some other piece."""
        connected = set()
        for position in self.positions:
            connected.update(self.empty_neighbours(position))
        return connected

    def new_placements(self):
        """Valid placements for a new piece. These are connected placements not neighbouring any opponent's pieces."""
        opponent_connected = set()
        for (position, piece) in self.positions.items():
            if piece.player != self.next_player:
                opponent_connected.update(self.empty_neighbours(position))
        return self.connected_placements() - opponent_connected

    def my_neighbours(self, position):
        """Neighbouring positions with next player's piece"""
        return self.neighbours(position, self.next_player)

    def opponent_neighbours(self, position):
        """Neighbouring positions with opponent's piece"""
        return (p for p in self.neighbours(position) if self.positions(p).player != player)

    def empty_neighbours(self, position):
        """Neighbouring positions without a piece"""
        return (p for p in self.directions(position) if p not in self.positions)

    def neighbours(self, position, player):
        """Neighbouring positions for specified player"""
        return (p for p in self.directions(position) if p in self.positions and self.positions(p).player == player)

    def directions(self, position):
        """Valid neighbouring positions"""
        (x, y) = position
        return [(x, y - 1), (x - 1, y + 1), (x, y + 1), (x - 1, y), (x - 1, y), (x - 1, y - 1)]

    def __str__(self):
        return "not implemented"


class Piece:
    def  __init__(self, insect, player):
        # Insect
        self.insect = insect
    
        # Player number 
        self.player = player


