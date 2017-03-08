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
    # print(game.to_string())
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # print("score={} player={}".format(float(own_moves - opp_moves), player))
    return float(own_moves - opp_moves)

class CustomPlayer:
    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        self.game = game
        self.time_left = time_left
        try:
            if not legal_moves:
                return (-1, -1)

            self.legal_moves = legal_moves
            self.best_move = legal_moves[0]
            _, self.best_move = self.minimax(self.game, 1, True)
            return self.best_move

        except Timeout:
            print("timeout")
            print(game.to_string())
            print(self.best_move)
            # Handle any actions required at timeout, if necessary
            return self.best_move

    def minimax(self, game, depth, maximizing_player=True):
        self.game = game
        self.maximizing_player = maximizing_player
        best_move = (-1, -1)

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if(depth > 0):
            best_move = None
            # print("depth {}".format(depth))
            if maximizing_player:
                best_score = float("-inf")
                # for move in tmp_moves:
                for move in self.game.get_legal_moves():
                    # print("max move={}".format(move))
                    tmp_score, _ = self.minimax(game.forecast_move(move), depth - 1, not maximizing_player)
                    # if there is no best_move, save the first move
                    if(best_move == None or tmp_score > best_score):
                        best_score = tmp_score
                        best_move = move
            else:
                best_score = float("inf")
                # for move in tmp_moves:
                for move in self.game.get_legal_moves():
                    # print("Min move={}".format(move))
                    tmp_score, _ = self.minimax(game.forecast_move(move), depth - 1, not maximizing_player)
                    # if there is no best_move, save the first move
                    if(best_move == None or tmp_score < best_score):
                        best_score = tmp_score
                        best_move = move

            # print("end depth {} best move={} best_score={}".format(depth, best_move, best_score))
            return best_score, best_move

        if(depth == 0):
            best_move = None
            # print("depth 0")
            if maximizing_player:
                best_score = float("-inf")
                # for move in tmp_moves:
                for move in self.game.get_legal_moves():
                    tmp_score = self.score(self.game.forecast_move(move), self.game.active_player)
                    # print("depth 0 Max move={} tmp_score={}".format(move, tmp_score))
                    if (best_move == None or tmp_score > best_score):
                        # print("depth 0 Max best")
                        best_score = tmp_score
                        best_move = move
                # print("end depth 0 if")
            else:
                best_score = float("-inf")
                # for move in tmp_moves:
                for move in self.game.get_legal_moves():
                    #find my score after the opponent moves
                    tmp_score = self.score(self.game.forecast_move(move), self.game.inactive_player)
                    # print("depth 0 Min move={} tmp_score={}".format(move, tmp_score))
                    #keep the lowest score, because that is what the opponent will do
                    if (best_move == None or tmp_score > best_score):
                        # print("depth 0 Min best")
                        best_score = tmp_score
                        best_move = move
                # print("end depth 0 else opponent best_move={} best_score={}".format(best_move, best_score))

        return best_score, best_move

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
