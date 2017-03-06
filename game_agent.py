"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # print(game.to_string())
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
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
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.game = game
        self.time_left = time_left


        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if not legal_moves:
                return (-1, -1)

            self.legal_moves = legal_moves
            #set the best move to the first legal move incase there is an issue with time
            self.best_move = legal_moves[0]

            self.best_move = self.minimax(self.game, 2, True)

            # depth = 2
            # counter = 0
            # while (counter < depth):
            #     counter = counter + 1
            #     for move in bottom_row.get_bottom_row():
            #         move.get_opponents_moves(self.still_have_time)

            return self.best_move

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return self.best_move

    def still_have_time(self):
        # import time
        # # time_limit = 1.90
        # time_limit = 5.90
        # return (time.time() - self.start_time < time_limit)
        return True

    def minimax(self, game, depth, maximizing_player=True):

        print("minimax depth={} maximizing_player={}".format(depth, maximizing_player))
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """


        self.game = game
        self.depth = depth
        self.maximizing_player = maximizing_player

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # for current_move in self.game.get_legal_moves():
        #
        #
        # self.board_post_move = self.game.forecast_move(current_move)
        #
        # self.best_move = max(self.my_moves_this_level, key=lambda move: move.get_my_score_post_move())
        # self.worst_move = min(self.my_moves_this_level, key=lambda move: move.get_my_score_post_move())

        # temp_best_move = ''
        # for current_move in self.game.get_legal_moves():
        #     print("current_move={}".format(current_move))
        #     my_score = self.score(self.game.forecast_move(current_move), self.game.active_player if maximizing_player else self.game.inactive_player)
        #     print("minimax={}".format(my_score))

        # print ("minimax depth={} self.maximizing_player={}".format(self.depth, self.maximizing_player))
        # print(self.game.to_string())
        #
        # self.max_score =  float("-inf") if maximizing_player else float("inf")
        # for sample_move in self.game.get_legal_moves():
        #     tmp_game = self.game.forecast_move(sample_move)
        #     tmp_score = self.score(tmp_game, self.game.active_player)
        #     if maximizing_player:
        #         if(self.max_score < tmp_score):
        #             self.max_score = tmp_score
        #     else:
        #         if(self.max_score > tmp_score):
        #             self.max_score = tmp_score
        #
        #     print("self.max_score={}".format(self.max_score))
        #
        #     while self.depth > 1:
        #         return_value = self.minimax(tmp_game, self.depth - 1, not self.maximizing_player)
        #         print("return_value={}".format(return_value))

        # if(self.depth == 1):
        #     if maximizing_player:
        #         max_move = max(self.game.get_legal_moves(), key=lambda current_move: self.score(self.game.forecast_move(current_move), self.game.active_player))
        #     else:
        #         max_move = min(self.game.get_legal_moves(), key=lambda current_move: self.score(self.game.forecast_move(current_move), self.game.inactive_player))
        # else:
        #     self.minimax(tmp_game, self.depth - 1, not self.maximizing_player)

        # if maximizing_player:
        #     max_move = max(self.game.get_legal_moves(), key=lambda current_move: self.score(self.game.forecast_move(self.minimax(self.game, depth -1, not self.maximizing_player)), self.game.active_player))
        # else:
        #     max_move = max(self.game.get_legal_moves(), key=lambda current_move: self.score(self.game.forecast_move(self.minimax(self.game, depth -1, not self.maximizing_player)), self.game.inactive_player))

        if maximizing_player:
            max_move = max(self.game.get_legal_moves(), key=lambda current_move: self.score(self.game.forecast_move(current_move), self.game.active_player))
        else:
            max_move = min(self.game.get_legal_moves(), key=lambda current_move: self.score(self.game.forecast_move(current_move), self.game.inactive_player))

        # if maximizing_player:
        #     max_move = max(self.game.get_legal_moves(), key=lambda current_move: self.score(self.game.forecast_move(current_move), self.game.active_player))
        # else:
        #     max_move = min(self.game.get_legal_moves(), key=lambda current_move: self.score(self.game.forecast_move(current_move), self.game.inactive_player))
            # print("here")
            # print(self.game.to_string())
            # legal_moves = self.game.get_legal_moves()
            # score_pre = self.score(self.game, self.game.inactive_player)
            # tmp_game = self.game.forecast_move(legal_moves[0])
            # score_post = self.score(tmp_game, self.game.inactive_player)
            # print("score_pre={} score_post={}".format(score_pre, score_post))


        # return
        # while self.depth > 1:
        #     self.depth = self.depth - 1
        #     print (self.depth)
        #     return self.minimax(self.game, self.depth, not self.maximizing_player)

        print("max_move={}", max_move)
        return max_move

            # self.my_moves_this_level = []
        #
        # for possible_move in self.legal_moves:
        #     current_move = SingleMove(self.game, possible_move)
        #     self.my_moves_this_level.append(current_move)
        #
        # counter = 0
        # while (counter < depth):
        #     counter = counter + 1
        #     for move in bottom_row.get_bottom_row():
        #         move.get_opponents_moves(self.still_have_time)
        #
        #
        #
        # self.best_move = max(self.my_moves_this_level, key=lambda move: move.get_my_score_post_move()).get_my_move()


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        raise NotImplementedError
