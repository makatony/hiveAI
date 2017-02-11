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
        # stack of available pieces: player number -> (insect -> count)
        self.stack = dict((player, { ANT: 3, BEETLE: 2, GRASSHOPPER: 3, QUEEN: 1, SPIDER: 2 }) for player in range(PLAYERS))

        # map of position: (x,y) -> Piece
        self.positions = positions
        for (position, piece) in positions.items():
            self.stack[piece.player][piece.insect] = max(self.stack[piece.player][piece.insect] - 1, 0)

        # next player number
        self.next_player = 0

    def neighbours(self, position, player):
        """Neighbouring pieces for specified position and player"""
        return (p for p in self.directions(position) if p in self.positions and self.positions(p).player == player)

    def my_neighbours(self, position):
        """Neighbouring pieces owned by the next player for specified position"""
        return self.neighbours(position, self.next_player)

    def opponent_neighbours(self, position):
        """Neighbouring pieces owned by the opponents for specified position"""
        return (p for p in self.neighbours(position) if self.positions(p).player != player)

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


