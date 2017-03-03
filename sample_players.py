"""This file contains a collection of player classes for comparison with your
own agent and example heuristic functions.
"""

from random import randint


def null_score(game, player):
    """This heuristic presumes no knowledge for non-terminal states, and
    returns the same uninformative value for all other states.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return 0.


def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


def improved_score(game, player):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


class RandomPlayer():
    """Player that chooses a move randomly."""

    def get_move(self, game, legal_moves, time_left):
        """Randomly select a move from the available legal moves.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            A randomly selected legal move; may return (-1, -1) if there are
            no available legal moves.
        """

        if not legal_moves:
            return (-1, -1)
        return legal_moves[randint(0, len(legal_moves) - 1)]


class GreedyPlayer():
    """Player that chooses next move to maximize heuristic score. This is
    equivalent to a minimax search agent with a search depth of one.
    """

    def __init__(self, score_fn=open_move_score):
        self.score = score_fn

    def get_move(self, game, legal_moves, time_left):
        """Select the move from the available legal moves with the highest
        heuristic score.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            The move in the legal moves list with the highest heuristic score
            for the current game state; may return (-1, -1) if there are no
            legal moves.
        """

        if not legal_moves:
            return (-1, -1)
        _, move = max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])
        return move


class HumanPlayer():
    """Player that chooses a move according to user's input."""

    def get_move(self, game, legal_moves, time_left):
        """
        Select a move from the available legal moves based on user input at the
        terminal.

        **********************************************************************
        NOTE: If testing with this player, remember to disable move timeout in
              the call to `Board.play()`.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            The move in the legal moves list selected by the user through the
            terminal prompt; automatically return (-1, -1) if there are no
            legal moves
        """
        if not legal_moves:
            return (-1, -1)

        print(('\t'.join(['[%d] %s' % (i, str(move)) for i, move in enumerate(legal_moves)])))

        valid_choice = False
        while not valid_choice:
            try:
                index = int(input('Select move index:'))
                valid_choice = 0 <= index < len(legal_moves)

                if not valid_choice:
                    print('Illegal move! Try again.')

            except ValueError:
                print('Invalid index! Try again.')

        return legal_moves[index]


class MyMove(object):
    def __init__(self, board, player_is_me, current_move, depth, counter=0):
        global number_of_nodes
        number_of_nodes = number_of_nodes + 1
        self.board = board
        self.player_is_me = player_is_me
        self.current_move = current_move
        self.depth = depth
        self.counter = counter
        self.opponents_moves = []

        self.board_after_move = self.board.forecast_move(self.current_move)
        self.create_opponents_moves()

        print("player_is_me: {} current_move {} depth {} counter {}".format(self.player_is_me, self.current_move, self.depth, self.counter))
    def create_opponents_moves(self):
        # while self.counter <= self.depth:
            for potential_move in self.board.get_legal_moves():
                self.opponents_moves.append(MyMove(self.board_after_move, self.player_is_me, potential_move, self.depth, self.counter))
            # self.counter = self.counter + 1


    def display(self):
        print("player_is_me: {} current_move {} depth {} counter {}".format(self.player_is_me, self.current_move, self.depth, self.counter))
        own_moves = len(self.board.get_legal_moves(self.board.active_player))
        opp_moves = len(self.board.get_legal_moves(self.board.inactive_player))
        print("own_moves: {}, opp_moves: {}".format(own_moves, opp_moves))
        improved_my_score = improved_score(self.board, self.board.active_player)
        print("improved_my_score: {}".format(improved_my_score))
        # print(self.board_after_move.to_string())
        print("--------------Children-----------------")
        for move in self.opponents_moves:
            move.display()


def print_possible_moves(board, player1, player2):
    player1_moves = board.get_legal_moves(player1)
    player2_moves = board.get_legal_moves(player2)
    print("player1 {}: {} player2 {}: {}".format(len(player1_moves), player1_moves, len(player2_moves), player2_moves))

class BottomRow(object):
    def __init__(self):
        self.bottom_depth = -1
        self.bottom_nodes = []
    def registerNode(self, node, depth):
        if(depth > self.bottom_depth):
            self.bottom_depth = depth
            self.bottom_nodes = []
            self.bottom_nodes.append(node)
        else:
            self.bottom_nodes.append(node)
    def get_bottom_row(self):
        return self.bottom_nodes
    def reset(self):
        self.bottom_depth = -1
        self.bottom_nodes = []
    def display(self):
        print("bottom_depth: {}".format(self.bottom_depth))
        for node in self.bottom_nodes:
            print("node move: {}".format(node.get_my_move()))

class SingleMove(object):
    global bottom_row
    def __init__(self, board, current_move, active_player, inactive_player, max_depth, current_depth):
        global number_of_nodes
        self.board = board
        self.current_move = current_move
        self.active_player = active_player
        self.inactive_player = inactive_player
        self.improved_score_pre_move = improved_score(self.board, self.active_player)
        self.board_post_move = self.board.forecast_move(current_move)
        self.improved_score_post_move = improved_score(self.board_post_move, self.active_player)
        self.max_depth = max_depth
        self.current_depth = current_depth
        self.opponents_moves = []

        number_of_nodes = number_of_nodes + 1

        # print("current_move: {}".format(current_move))
        # print("improved_score_pre_move: {} improved_score_post_move: {}".format(self.improved_score_pre_move, self.improved_score_post_move))
        # print_possible_moves(self.board_post_move, self.active_player, self.inactive_player)
        # print('')
        bottom_row.registerNode(self, current_depth)

    def get_new_board(self):
        return self.board_post_move

    def get_my_score_post_move(self):
        return self.improved_score_post_move
    def get_my_move(self):
        return self.current_move
    def get_opponents_moves(self):
        opponents_moves = self.board_post_move.get_legal_moves(self.inactive_player)
        for possible_move in opponents_moves:
            current_move = SingleMove(self.board_post_move, possible_move, self.board.inactive_player, self.board.active_player, self.max_depth, self.current_depth + 1)
            self.opponents_moves.append(current_move)



class GetMove(object):
    def __init__(self, board, player_is_me, depth, counter=0):
        global bottom_row
        self.board = board
        self.player_is_me = player_is_me
        self.depth = depth
        self.counter = counter
        self.opponents_moves = []

        self.my_possible_moves = self.board.get_legal_moves()
        self.my_moves_this_level = []
        # for my_moves in self.my_possible_moves:

        # print("player_is_me: {} depth: {} counter: {}".format(self.player_is_me, self.depth, self.counter))
        print_possible_moves(self.board, self.board.active_player, self.board.inactive_player)

        #explore all of my current level moves
        for possible_move in self.my_possible_moves:
            current_move = SingleMove(self.board, possible_move, self.board.active_player, self.board.inactive_player, depth, counter)
            self.my_moves_this_level.append(current_move)

        best_move = max(self.my_moves_this_level, key=lambda move: move.get_my_score_post_move())
        worst_move = min(self.my_moves_this_level, key=lambda move: move.get_my_score_post_move())
        # print("best_move: {} best_score: {} worst_move: {} worst_score: {}".format(best_move.get_my_move(), best_move.get_my_score_post_move(), worst_move.get_my_move(), worst_move.get_my_score_post_move()))

        # for move in self.my_moves_this_level:
        #     print("move: {} score: {}".format(move.get_my_move(), move.get_my_score_post_move()))
        #
        # print("--------------------------------------")

    def print_results(self):
        print("")
        print("------RESULTS-------")
        for my_move_at_this_level in self.my_moves_this_level:
            print("move: {} get_my_score_post_move:{}".format(my_move_at_this_level.get_my_move(), my_move_at_this_level.get_my_score_post_move()))

    def display(self):
        print("player_is_me: {} depth {} counter {}".format(self.player_is_me, self.depth, self.counter))
        print("my possible moves {}".format(self.my_possible_moves))


def new_test():
    global bottom_row
    bottom_row = BottomRow()

    global number_of_nodes
    number_of_nodes = 0
    import time
    start_time = time.time()
    from isolation import Board
    player1 = RandomPlayer()
    player2 = RandomPlayer()
    board = Board(player1, player2)

    available_moves = board.get_legal_moves(player1)
    board.apply_move(available_moves[0])
    available_moves = board.get_legal_moves(player2)
    board.apply_move(available_moves[0])
    available_moves = board.get_legal_moves(player1)
    board.apply_move(available_moves[0])
    available_moves = board.get_legal_moves(player2)
    board.apply_move(available_moves[0])
    # print("Starting board")
    # print(board.to_string())

    move = GetMove(board, True, 1)
    # print("move={}".format(move.get_move()))
    # move.display()
    # bottom_row.display()

    for move in bottom_row.get_bottom_row():
        move.get_opponents_moves()

    for move in bottom_row.get_bottom_row():
        move.get_opponents_moves()

    for move in bottom_row.get_bottom_row():
        move.get_opponents_moves()
    for move in bottom_row.get_bottom_row():
        move.get_opponents_moves()
    for move in bottom_row.get_bottom_row():
        move.get_opponents_moves()
    for move in bottom_row.get_bottom_row():
        move.get_opponents_moves()

    time_taken = time.time() - start_time

    bottom_row.display()
    print("time taken {}".format(time_taken))
    print("number of nodes {}".format(number_of_nodes))
    print(bottom_row.get_bottom_row()[0].get_new_board().to_string())


if __name__ == "__main__":
    new_test()