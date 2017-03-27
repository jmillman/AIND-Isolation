"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math

def custom_score_diff_in_free_percent_of_board(game, player):
    #this will take the percentage the free spaces I can move to - the percentage of free spaces an opponent can move to
    #this should weight more heavily for me when the opponent  has a smaller number of moves
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blank_spaces = len(game.get_blank_spaces())
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    my_free_percent = own_moves / blank_spaces
    opp_free_percent = opp_moves / blank_spaces
    diff_in_free_percent = my_free_percent - opp_free_percent
    return float(diff_in_free_percent)

def custom_score_diff_in_mine_and_double_opponent(game, player):
    #simply take the difference in my moves - (2 * opponentes moves), should weight 2 to 1 better than 5 to 4
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    diff = own_moves - (2 * opp_moves)
    return float(diff)

def custom_score_divide_own_by_opponent(game, player):
    #divide my moves by the opponent
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    if(opp_moves == 0):
        return float("inf")
    return float(own_moves / opp_moves)

def custom_score_diff_in_mine_and_double_opponent_chase_incase_of_tie(game, player):
    #take the difference in my moves - (2 * opponentes moves)
    #then double the number and subtract the distance away, meaning it will rank higher for moves closer to the opponent
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    diff = own_moves - (2 * opp_moves)

    own_location = game.get_player_location(player)
    opp_location = game.get_player_location(game.get_opponent(player))
    dist_between_locations = math.hypot(own_location[0] - opp_location[0], own_location[1] - opp_location[1])

    #still want to make the main driver the differenc in locations, and don't want the distance to factor too much into, so double the diff
    return float(diff * 2 - dist_between_locations)

def custom_score_diff_in_mine_and_double_opponent_run_away_incase_of_tie(game, player):
    # take the difference in my moves - (2 * opponentes moves)
    # then double the number and add the distance away, meaning it will rank higher for moves away from the opponent
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    diff = own_moves - (2 * opp_moves)

    own_location = game.get_player_location(player)
    opp_location = game.get_player_location(game.get_opponent(player))
    dist_between_locations = math.hypot(own_location[0] - opp_location[0], own_location[1] - opp_location[1])

    # still want to make the main driver the differenc in locations, and don't want the distance to factor too much into, so double the diff
    return float(diff * 2 + dist_between_locations)

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
    return custom_score_diff_in_mine_and_double_opponent_run_away_incase_of_tie(game, player)

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
                 iterative=True, method='minimax', timeout=15.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

        self.move_count = 0

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
            else:
                best_move = legal_moves[0]
                best_score = float("-inf")

            # print("")
            self.move_count += 1
            player_number = game.__player_symbols__[game.active_player]
            # print("GET MOVE START********************** blank_spaces // 2 = {} move_count = {} I am {} legal_moves {}".format(len(game.get_blank_spaces()) // 2, self.move_count, player_number, legal_moves))
            # print(game.to_string())

            if(self.method == 'minimax'):
                if(self.iterative):
                    temp_depth = 1
                    while True:
                    # while temp_depth <= (len(legal_moves)):
                        tmp_score, tmp_best_move = self.minimax(game, temp_depth, True, True)
                        if(tmp_score > float("-inf")):
                            best_move = tmp_best_move
                            best_score = tmp_score
                        # print("MM move returned = {}, score = {}".format(best_move, tmp_score))
                        temp_depth += 1
                else:
                    tmp_score, best_move = self.minimax(game, self.search_depth, True, True)
            elif(self.method == 'alphabeta'):
                if(self.iterative):
                    temp_depth = 1
                    while True:
                    # while temp_depth <= (len(legal_moves)):
                        tmp_score, tmp_best_move = self.alphabeta(game, temp_depth, float("-inf"), float("inf"), True, True)
                        if(tmp_score > float("-inf")):
                            best_move = tmp_best_move
                            best_score = tmp_score
                        # print("AB move returned = {}, score = {}".format(best_move, tmp_score))
                        temp_depth += 1
                else:
                    tmp_score, best_move = self.alphabeta(game, self.search_depth, float("-inf"), float("inf"), True, True)
            else:
                raise

            # try:
            # print("************LEGIT No timer*****************")
            # print("move = {} score = {}".format(best_move, best_score))
            # print("legal_moves= {}".format(legal_moves))
            # print("I am player {}".format(player_number))
            # print(game.to_string())
            # except:
            #     print("GET MOVE END move used = {} score = {}".format(best_move, "No Score"))
            return best_move

        except Timeout:
            # print("************TIMEOUT*****************")
            # print("move = {} score = {}".format(best_move, best_score))
            # print("legal_moves= {}".format(legal_moves))
            # print("I am player {}".format(player_number))
            # own_moves = len(game.get_legal_moves(game.active_player))
            # opp_moves = len(game.get_legal_moves(game.get_opponent(game.active_player)))
            # print("own_moves = {} opp_moves = {}".format(own_moves, opp_moves))
            # print(game.to_string())
            # print(game.to_string())

            # print(game.to_string())
            # Handle any actions required at timeout, if necessary
            return best_move

    def minimax(self, game, depth, maximizing_player=True, is_root_move = False):
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
        # best_move = (-1, -1)

        # if(is_root_move):
        #     print("ROOT MOVE minimax********************")
        # print("minimax depth = {}".format(depth))

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return float("-inf"), (-1, -1)

        best_move = legal_moves[0]

        if(depth > 1):
            # print("depth {}".format(depth))
            if maximizing_player:
                best_score = float("-inf")
                # for move in tmp_moves:
                for move in legal_moves:
                    # print("depth {} {} move={}".format(depth, 'Max' if maximizing_player else 'min', move))
                    # print("max move={}".format(move))
                    tmp_score, _ = self.minimax(game.forecast_move(move), depth - 1, not maximizing_player)
                    # print("depth {} Max move={} tmp_score={}".format(depth, move, tmp_score))
                    # if there is no best_move, save the first move
                    if(best_move == None or tmp_score > best_score):
                        best_score = tmp_score
                        best_move = move
            else:
                best_score = float("inf")
                # for move in tmp_moves:
                for move in legal_moves:
                    # print("depth {} {} move={}".format(depth, 'Max' if maximizing_player else 'min', move))
                    # print("Min move={}".format(move))
                    tmp_score, _ = self.minimax(game.forecast_move(move), depth - 1, not maximizing_player)
                    # print("depth {} Min move={} tmp_score={}".format(depth, move, tmp_score))
                    # if there is no best_move, save the first move
                    if(best_move == None or tmp_score < best_score):
                        best_score = tmp_score
                        best_move = move
        if(depth == 1):
            # print("depth 0")
            if maximizing_player:
                best_score = float("-inf")
                # for move in tmp_moves:
                for move in legal_moves:
                    tmp_score = self.score(game.forecast_move(move), game.active_player)
                    # print("depth {} {} move={} tmp_score={}".format(depth, 'Max' if maximizing_player else 'min', move, tmp_score))
                    if (best_move == None or tmp_score > best_score):
                        # print("depth 0 Max best")
                        best_score = tmp_score
                        best_move = move
                # print("end depth 0 if")
            else:
                best_score = float("-inf")
                # for move in tmp_moves:
                for move in legal_moves:
                    #find my score after the opponent moves
                    tmp_score = self.score(game.forecast_move(move), game.inactive_player)
                    # print("depth {} {} move={} tmp_score={}".format(depth, 'Max' if maximizing_player else 'min', move, tmp_score))
                    #keep the lowest score, because that is what the opponent will do
                    if (best_move == None or tmp_score < best_score):
                        # print("depth 0 Min best")
                        best_score = tmp_score
                        best_move = move

        # print("minimax end depth {} {} best move={} best_score={}".format(depth, 'Max' if maximizing_player else 'min', best_move, best_score))
        return best_score, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True, is_root_move = False):
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

        # if(is_root_move):
        #     print("ROOT MOVE alphabeta******************** depth = {}".format(depth))
        # print("alphabeta depth = {}".format(depth))

        # if (len(game.get_blank_spaces()) // 2 <= 6):
        #     print(game.to_string())
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return float("-inf"), (-1, -1)

        best_move = legal_moves[0]

        if(depth > 1):
            if maximizing_player:
                best_score = float("-inf")
                # for move in tmp_moves:
                for move in legal_moves:
                    # print("alpha beta attempting move = {} depth = {} {}".format(move, depth, 'Max' if maximizing_player else 'MIN'))
                    tmp_score, _ = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, not maximizing_player)
                    # print("alpha beta attempted move = {} it's score = {} {}".format(move, tmp_score, 'Max' if maximizing_player else 'MIN'))
                    # if there is no best_move, save the first move
                    alpha = max(tmp_score, alpha)
                    if(beta <= alpha):
                        # best_score = tmp_score
                        break
                    if(best_move == None or tmp_score > best_score):
                        best_score = tmp_score
                        best_move = move
            else:
                best_score = float("inf")
                # for move in tmp_moves:
                for move in legal_moves:
                    # print("alpha beta attempting move = {} depth = {} {}".format(move, depth, 'Max' if maximizing_player else 'MIN'))
                    tmp_score, _ = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, not maximizing_player)
                    # print("alpha beta attempted move = {} it's score = {} {}".format(move, tmp_score, 'Max' if maximizing_player else 'MIN'))
                    # if there is no best_move, save the first move
                    beta = min(tmp_score, beta)
                    if(beta <= alpha):
                        # best_score = tmp_score
                        break
                    if(best_move == None or tmp_score < best_score):
                        best_score = tmp_score
                        best_move = move

        if(depth == 1):
            if maximizing_player:
                best_score = float("-inf")
                # for move in tmp_moves:
                for move in legal_moves:
                    tmp_score = self.score(game.forecast_move(move), game.active_player)
                    # print("alpha beta depth 1 move = {} it's score = {} {}".format(move, tmp_score, 'Max' if maximizing_player else 'MIN'))

                    alpha = max(tmp_score, alpha)
                    if(beta <= alpha):
                        # best_score = tmp_score
                        break
                    if (best_move == None or tmp_score > best_score):
                        best_score = tmp_score
                        best_move = move
            else:
                best_score = float("-inf")
                # for move in tmp_moves:
                for move in legal_moves:
                    #find my score after the opponent moves
                    tmp_score = self.score(game.forecast_move(move), game.inactive_player)
                    # print("alpha beta depth 1 move = {} it's score = {} {}".format(move, tmp_score, 'Max' if maximizing_player else 'MIN'))
                    beta = min(tmp_score, beta)
                    if(beta <= alpha):
                        # best_score = tmp_score
                        break
                    #keep the lowest score, because that is what the opponent will do
                    if (best_move == None or tmp_score < best_score):
                        best_score = tmp_score
                        best_move = move
                # print("end depth 0 else opponent best_move={} best_score={}".format(best_move, best_score))

        # print("alpha beta end depth {} {} best move={} best_score={}".format(depth, 'Max' if maximizing_player else 'MIN', best_move, best_score))
        return best_score, best_move