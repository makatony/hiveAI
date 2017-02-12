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
        new_placements = None
        player_stack = self.stack[self.next_player]
        must_play_queen = player_stack[QUEEN] > 0 and len(tuple(self.my_pieces())) >= 3
        for insect, count in player_stack.items():
            if must_play_queen and insect != QUEEN:
                continue
            if count > 0:
                if new_placements is None:
                    new_placements = self.new_placements()
                for target_position in new_placements:
                    yield (insect, None, target_position)
        if player_stack[QUEEN] > 0:
            # No moves while queen is not placed.
            return

        # Moves per piece.
        for src_position, piece in self.positions.items():
            if piece.player != self.next_player:
                continue
            if not self.removable(src_position):
                continue

            tgt_positions = []
            if piece.insect == QUEEN:
                tgt_positions = self.queen_moves(src_position)
            
            # We have the piece and the target positions, just
            # enumerate them.
            for tgt_position in tgt_positions:
                yield (piece.insect, src_position, tgt_position)

    def queen_moves(self, src_position):
        """Enumerate queen's move from src_position, assuming she can move."""
        return self.valid_next_steps(src_position, original_position=src_position, invalid=set(src_position))


    def removable(self, position):
        """Determine whether a piece on specified position is removable without splitting the hive."""
        #TODO: check if beetle is on top of anything, if that is the case, then it's removable.

        start_neighbours = list(self.occupied_neighbours(position))

        # Trivial cases: only one neighbor; and 5 or 6 neighbors, in which case they will forceabley
        # stay connected. 
        if len(start_neighbours) < 2 or len(start_neighbours) > 4:
            return True

        # Starting from one of the neighbors (start_neighbours[0]), all other have to be reached. 
        visited = set()
        visited.add(position)

        # temaining is the list of pieces we need to reach to prove that the graph will still be
        # connected.
        remaining = set(start_neighbours[:1])

        # to_visit is the next list of nodes to visit in our BFS.
        to_visit = set((start_neighbours[0],))
        while to_visit:
            new_to_visit = set()
            for visit in to_visit:
                for position in self.occupied_neighbours(visit):
                    if position in visited:
                        continue
                    visited.add((position,))
                    if position in remaining:
                        remaining.remove(position)
                        if not remaining:
                            return True
                    new_to_visit.update((position,))
            to_visit = new_to_visit
        return False

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

        # Filter out those positions that have any opponent as neighbour.
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

    def valid_next_steps(self, src_position, original_position, invalid):
        """Returns neighbouring positions that are empty but still connected to the graph.

        TODO: Check that piece is not "squeezing" through two other pieces.
        Args;
          position: where to search for the neighboors.
          original_position: where the piece is going to leave from, presumably will be 
            empty and therefore can't be used for invalid is a list of positions not valid to move to, and that shouldn't be
        considered for connectedness (presumably where the )...
        """
        for empty_pos in self.empty_neighbours(src_position):
            if empty_pos in invalid:
                continue
            for occupied_pos in self.occupied_neighbours(empty_pos):
                if occupied_pos != original_position:
                    # This position is connected, yield it and move to the next empty_pos
                    yield empty_pos
                    break


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


