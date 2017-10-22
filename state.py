# Piece type
ANT = "A"
BEETLE = "B"
GRASSHOPPER = "G"
QUEEN = "Q"
SPIDER = "S"

# Number of players
PLAYERS = 2


class Board:
    # We are playing on an hexagon-tiled map.
    NUM_NEIGHBOURS = 6

    def __init__(self, positions={}, covered={}):
        """Create a new board with specified positions of the pieces.

        Args:
            positions: map of position (x,y) to Piece object. Each piece
              provided will be automatically removed from the number of
              available pieces to add to the board.
            covered: this is a map of position (x,y) to a list of covered
              Piece objects (bottom-to-top). Covered Pieces happen when
              a Beetle move on top of them, in which case they are blocked
              and can't move, until the beetle moves.
        """
        # stack of available pieces: player number -> (insect -> count)
        self.stack = dict((player, {ANT: 3, BEETLE: 2, GRASSHOPPER: 3, QUEEN: 1, SPIDER: 2})
                          for player in range(PLAYERS))

        # map of position: (x,y) -> Piece
        self.positions = positions
        for position, piece in positions.items():
            self.stack[piece.player][piece.insect] = max(
                self.stack[piece.player][piece.insect] - 1, 0)

        # map of covered pieces: (x,y) -> Ordered (bottom-to-top) list of
        #   covered pieces.
        self.covered = covered
        for position, pieces in covered.items():
            for piece in pieces:
                self.stack[piece.player][piece.insect] = max(
                    self.stack[piece.player][piece.insect] - 1, 0)

        # next player number
        self.next_player = 0
        self.move_number = 0
        self.check_moves = False

    def valid_moves(self):
        """Yields tuple (insect, source_position, target_position) for each valid move."""
        # TODO: add support for no available move.

        # New placements.
        new_placements = None
        player_stack = self.stack[self.next_player]
        must_play_queen = player_stack[QUEEN] > 0 and len(
            tuple(self.my_pieces())) >= 3
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
            if not self.is_removable(src_position):
                continue

            tgt_positions = []
            if piece.insect == ANT:
                tgt_positions = self.ant_moves(src_position)
            elif piece.insect == QUEEN:
                tgt_positions = self.queen_moves(src_position)
            elif piece.insect == SPIDER:
                tgt_positions = self.spider_moves(src_position)
            elif piece.insect == GRASSHOPPER:
                tgt_positions = self.grasshopper_moves(src_position)
            elif piece.insect == BEETLE:
                tgt_positions = self.beetle_moves(src_position)

            # We have the piece and the target positions, just
            # enumerate them.
            for tgt_position in tgt_positions:
                yield (piece.insect, src_position, tgt_position)

    def move(self, move):
        """Move insect from source_position to target_position.

        Args:
            move: None (for skip move, only valid if there are no available moves), or
                a tuple of (insect, source_position, target_position).
        """
        if self.check_moves:
            valid = list(self.valid_moves())
            if len(valid) == 0:
                if move is not None:
                    raise ValueError('Move {} invalid, there are no valid moves, only option is None'.format(move))
            else:
                if move is None:
                    raise ValueError('There are {} valid moves, player cannot use None (no move)'.format(len(valid)))
                if not move in valid:
                    raise ValueError("Move {} is not valid. Possible moves are {}".format(move, valid))

        if move is not None:
            insect, src_position, tgt_position = move
            if src_position is None:
                if not self.stack[self.next_player][insect]:
                    raise ValueError("No %s piece left to place for player %d" %
                                     (insect, self.next_player))
                self.stack[self.next_player][insect] -= 1
                piece = Piece(insect, self.next_player)

            else:
                # Leaving from src_position.
                if self.is_empty(src_position):
                    raise ValueError("no piece in {}".format(src_position))
                if self.positions[src_position].insect != insect:
                    raise ValueError(
                        "piece in {} is not a {}, instead it is a {}".format(
                            src_position, insect, self.positions[src_position].insect))
                if self.positions[src_position].player != self.next_player:
                    raise ValueError(
                        "instect {} in {} does not belong to player {}".format(
                            insect, src_position, self.next_player))

                piece = self.positions[src_position]
                if src_position in self.covered:
                    self.positions[src_position] = self.covered[src_position].pop()
                    if not self.covered[src_position]:
                        self.covered.pop(src_position)
                else:
                    self.positions.pop(src_position)

            # Move piece to new location.
            if tgt_position in self.positions:
                if not tgt_position in self.covered:
                    self.covered[tgt_position] = [self.positions[tgt_position]]
                else:
                    self.covered[tgt_position].append(self.positions[tgt_position])
            self.positions[tgt_position] = piece

        # Switch players.
        self.next_player = 1 - self.next_player
        self.move_number += 1

    def neighbours(self, position):
        """Valid neighbouring positions, in circular order."""
        (x, y) = position
        if x % 2 == 0:
            return [(x, y - 1), (x + 1, y - 1), (x + 1, y), (x, y + 1), (x - 1, y), (x - 1, y - 1)]
        else:
            return [(x, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]

    def is_removable(self, position):
        """Determine whether a piece on specified position is removable without splitting the hive."""
        if self.is_on_top(position):
            # If there is a piece underneath, the top piece is always removable.
            return True

        start_neighbours = list(self.occupied_neighbours(position))

        # Trivial cases: only one neighbor; and 5 or 6 neighbors, in which case they will forceabley
        # stay connected.
        if len(start_neighbours) < 2 or len(start_neighbours) > 4:
            return True

        # print("start_neighbours=%s" % start_neighbours)

        # Starting from one of the neighbors (start_neighbours[0]), all other
        # have to be reached.
        visited = set()
        visited.add(position)

        # temaining is the list of pieces we need to reach to prove that the graph will still be
        # connected.
        remaining = set(start_neighbours[1:])

        # to_visit is the next list of nodes to visit in our BFS.
        to_visit = set((start_neighbours[0],))
        while to_visit:
            new_to_visit = set()
            for visit in to_visit:
                for position in self.occupied_neighbours(visit):
                    if position in visited:
                        continue
                    visited.add(position)
                    if position in remaining:
                        remaining.remove(position)
                        if not remaining:
                            return True
                    new_to_visit.add(position)
            to_visit = new_to_visit
        return False

    def new_placements(self):
        """Return tuple with valid placements for a new piece. These are connected placements not neighbouring any opponent's pieces."""
        # Trivial case: first piece in play:
        if len(self.positions) == 0:
            return ((0, 0),)

        # Second trivial case: second piece in play:
        if len(self.positions) == 1:
            return self.neighbours((0, 0))

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

    def is_occupied(self, position):
        return position in self.positions

    def is_empty(self, position):
        return position not in self.positions

    def is_on_top(self, position):
        return position in self.covered and self.covered[position]

    def occupied_neighbours(self, position):
        """Neighbouring positions with a piece"""
        return (pos for pos in self.neighbours(position) if self.is_occupied(pos))

    def empty_neighbours(self, position):
        """Neighbouring positions without a piece"""
        return (pos for pos in self.neighbours(position) if self.is_empty(pos))

    def empty_and_connected_neighbours(self, src_position, original_position, invalid):
        """Returns neighbouring positions that are empty but still connected to the graph.

        It also checks that piece is not "squeezing" through two other pieces.

        Args;
          src_position: from where this move starts.
          original_position: where the piece is going to leave from: this is equal to
            src_position for the first step of a piece, and then something different
            later on. Presumably will be empty and therefore can't be considered as
            an occupied neighboor.
          invalid: don't consider these positions.
        """
        neighbours = self.neighbours(src_position)
        occupied = [(self.is_occupied(pos) and pos != original_position)
                    for pos in neighbours]

        for ii in range(len(neighbours)):
            tgt_pos = neighbours[ii]

            if tgt_pos in invalid:
                continue

            if occupied[ii]:
                # Target destination must be empty.
                continue

            if occupied[(ii + 1) % Board.NUM_NEIGHBOURS] and occupied[(ii - 1) % Board.NUM_NEIGHBOURS]:
                # Squeeze between two pieces is not allowed.
                continue

            is_connected = False
            for connected_pos in self.neighbours(tgt_pos):
                if connected_pos == src_position or connected_pos == original_position:
                    # src_position and original_position are supposed to be
                    # empty.
                    continue
                if self.is_occupied(connected_pos):
                    # All good, position is connected, we only need one
                    # position.
                    is_connected = True
                    break
            if not is_connected:
                continue

            yield tgt_pos

    def __str__(self):
        return "not implemented"

    def queen_moves(self, src_position):
        """Enumerate queen's move from src_position, assuming she can move."""
        return self.empty_and_connected_neighbours(
            src_position, original_position=src_position, invalid=set([src_position]))

    def spider_moves(self, src_position):
        """Enumerate spider's moves from src_position: it must make 3 steps."""
        end_pos = set()
        path = [src_position]
        self._spider_moves_dfs(src_position, src_position, 3, end_pos, path)
        for pos in end_pos:
            yield(pos)

    def _spider_moves_dfs(self, src_position, original_position, depth, end_pos, path):
        depth -= 1
        if depth == 0:
            # Leaves of the DFS: these will the candidate end positions.
            for next_pos in self.empty_and_connected_neighbours(src_position, original_position, invalid=path):
                end_pos.add(next_pos)
        else:
            for next_pos in self.empty_and_connected_neighbours(src_position, original_position, invalid=path):
                path += [next_pos]
                self._spider_moves_dfs(
                    next_pos, original_position, depth, end_pos, path)
                path.pop()

    def grasshopper_moves(self, src_position):
        for direction in range(Board.NUM_NEIGHBOURS):
            steps, tgt_pos = self._grasshopper_next_free(
                src_position, direction)
            if steps > 1:
                yield(tgt_pos)

    def _grasshopper_next_free(self, src_position, direction):
        steps = 0
        next_pos = src_position
        while self.is_occupied(next_pos):
            next_pos = self.neighbours(next_pos)[direction]
            steps += 1
        return steps, next_pos

    def ant_moves(self, src_position):
        # to_visit is the next list of nodes to visit in our BFS.
        to_visit = set((src_position,))
        visited = set((src_position,))
        while to_visit:
            new_to_visit = set()
            for visit_pos in to_visit:
                visited.add(visit_pos)
                for next_visit in self.empty_and_connected_neighbours(visit_pos, src_position, invalid=[]):
                    if next_visit in visited or next_visit in to_visit:
                        continue
                    new_to_visit.add(next_visit)
            to_visit = new_to_visit
        for pos in visited:
            if pos != src_position:
                yield pos

    def beetle_moves(self, src_position):
        """Enumerate beetle's move from src_position, assuming it can move."""
        # If on top of a piece, it can move anywhere.
        if self.is_on_top(src_position):
            for pos in self.neighbours(src_position):
                yield pos
            return

        # It can always move on top of any neightbour.
        for pos in self.occupied_neighbours(src_position):
            yield pos

        # And it moves like the queen: notice that if not moving from the top,
        # it can't squeeze between pieces either.
        for pos in self.empty_and_connected_neighbours(
                src_position, original_position=src_position, invalid=set([src_position])):
            yield pos

    def end_of_game(self):
        """Returns whether the game is finished, and the winner.

        Returns:
            Tuple with game finished (bool) and winner: player number, or -1
            if a draw.
        """
        # Collects players with Queens with no empty neighbours.
        players_lost = []
        for position, piece in self.positions.items():
            if piece.insect == QUEEN and next(self.empty_neighbours(position), None) is None:
                players_lost.append(piece.player)
        for position, pieces in self.covered.items():
            for piece in pieces:
                if piece.insect == QUEEN and next(self.empty_neighbours(position), None) is None:
                    players_lost.append(piece.player)

        if players_lost:
            if len(players_lost) > 2 or len(set(players_lost)) != len(players_lost):
                raise ValueError(
                    'Invalid set of Queens sorounded: %{}'.format(players_lost))

        if len(players_lost) == 1:
            return (True, 1 - players_lost[0])
        elif len(players_lost) == 2:
            return (True, -1)

        # Check if there are any available moves.
        for _ in self.valid_moves():
            return (False, -1)
        self.next_player = 1 - self.next_player
        for _ in self.valid_moves():
            self.next_player = 1 - self.next_player
            return (False, -1)
        self.next_player = 1 - self.next_player

        # No more moves available.
        return (True, -1)


class Piece:

    def __init__(self, insect, player):
        # Insect
        self.insect = insect

        # Player number
        self.player = player
