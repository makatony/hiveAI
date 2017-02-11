# Piece type
ANT = "A"
BEETLE = "B"
GRASSHOPPER = "G"
QUEEN = "Q"
SPIDER = "S"

class Board:
    def __init__(self):
        # map of position: (x,y) -> Piece
        self.positions = {}

        # next player number
        self.next = 0

        # stack of available pieces: player number -> (insect -> count)
        self.stack = dict((player, { ANT: 3, BEETLE: 2, GRASSHOPPER: 3, QUEEN: 1, SPIDER: 2 }) for player in range(2))

    def __str__(self):
        return "not implemented"


class Piece:
    def  __init__(self, insect, player):
        # Insect
        self.insect = insect
    
        # Player number 
        self.player = player


