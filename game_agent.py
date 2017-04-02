"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math

def custom_score_simple(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    diff = own_moves - opp_moves
    return float(diff)

def custom_score_my_open_moves(game, player):
    #just rank moves according to what gives me the most options
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    return float(own_moves)

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

def custom_score_diff_in_opp_and_double_mine(game, player):
    #this is to test a bad scoring algorithm
    #simply take the difference in my opp - (2 * my moves), should weight 2 to 1 better than 5 to 4
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    diff = opp_moves - (2 * own_moves)
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

def custom_score_diff_in_mine_and_double_opponent_closest_to_center_tie(game, player):
    # take the difference in my moves - (2 * opponentes moves)
    # then double the number and subtract the distance away from the center, meaning it will rank higher for moves closest to the center
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    diff = own_moves - (2 * opp_moves)

    own_location = game.get_player_location(player)
    center_of_board = (game.height // 2, game.width // 2)
    dist_between_locations = math.hypot(own_location[0] - center_of_board[0], own_location[1] - center_of_board[1])

    # still want to make the main driver the differenc in locations, and don't want the distance to factor too much into, so double the diff
    return float(diff * 2 - dist_between_locations)

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
    return custom_score_divide_own_by_opponent(game, player)

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
                 iterative=True, method='minimax', timeout=50.):
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

            self.move_count += 1
            player_number = game.__player_symbols__[game.active_player]

            if(self.method == 'minimax'):
                if(self.iterative):
                    temp_depth = 1
                    while True:
                        tmp_score, tmp_best_move = self.minimax(game, temp_depth, True)
                        if(tmp_score > float("-inf")):
                            best_move = tmp_best_move
                            best_score = tmp_score
                        else:
                            break
                        temp_depth += 1
                else:
                    tmp_score, best_move = self.minimax(game, self.search_depth, True)
            elif(self.method == 'alphabeta'):
                if(self.iterative):
                    temp_depth = 1
                    while True:
                        tmp_score, tmp_best_move = self.alphabeta(game, temp_depth, float("-inf"), float("inf"), True)
                        if(tmp_score > float("-inf")):
                            best_move = tmp_best_move
                            best_score = tmp_score
                        else:
                            break
                        if (best_move == None):
                            print(game.to_string())
                            tmp_score, tmp_best_move = self.alphabeta(game, temp_depth, float("-inf"), float("inf"), True)

                        temp_depth += 1
                else:
                    tmp_score, best_move = self.alphabeta(game, self.search_depth, float("-inf"), float("inf"), True)
            else:
                raise

            return best_move

        except Timeout:
            return best_move

    def minimax(self, game, depth, maximizing_player=True):
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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return float("-inf"), (-1, -1)

        best_move = None

        if(depth > 1):
            # print("depth {}".format(depth))
            if maximizing_player:
                best_score = float("-inf")
                for move in legal_moves:
                    tmp_score, _ = self.minimax(game.forecast_move(move), depth - 1, not maximizing_player)
                    # if there is no best_move, save the first move
                    if(best_move == None or tmp_score > best_score):
                        best_score = tmp_score
                        best_move = move
            else:
                best_score = float("inf")
                for move in legal_moves:
                    tmp_score, _ = self.minimax(game.forecast_move(move), depth - 1, not maximizing_player)
                    # if there is no best_move, save the first move
                    if(best_move == None or tmp_score < best_score):
                        best_score = tmp_score
                        best_move = move
        if(depth == 1):
            if maximizing_player:
                best_score = float("-inf")
                for move in legal_moves:
                    tmp_score = self.score(game.forecast_move(move), game.active_player)
                    if (best_move == None or tmp_score > best_score):
                        best_score = tmp_score
                        best_move = move
            else:
                best_score = float("-inf")
                for move in legal_moves:
                    #find my score after the opponent moves
                    tmp_score = self.score(game.forecast_move(move), game.inactive_player)
                    #keep the lowest score, because that is what the opponent will do
                    if (best_move == None or tmp_score < best_score):
                        best_score = tmp_score
                        best_move = move

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

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return float("-inf"), (-1, -1)

        best_move = None

        if(depth > 1):
            if maximizing_player:
                best_score = float("-inf")
                for move in legal_moves:
                    tmp_score, _ = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, not maximizing_player)
                    # if there is no best_move, save the first move
                    alpha = max(tmp_score, alpha)
                    if(best_move == None or tmp_score > best_score):
                        best_score = tmp_score
                        best_move = move
                    if(beta <= alpha):
                        best_score = tmp_score
                        break
            else:
                best_score = float("inf")
                for move in legal_moves:
                    tmp_score, _ = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, not maximizing_player)
                    # if there is no best_move, save the first move
                    beta = min(tmp_score, beta)
                    if(best_move == None or tmp_score < best_score):
                        best_score = tmp_score
                        best_move = move
                    if(beta <= alpha):
                        best_score = tmp_score
                        break

        if(depth == 1):
            if maximizing_player:
                best_score = float("-inf")
                for move in legal_moves:
                    tmp_score = self.score(game.forecast_move(move), game.active_player)
                    alpha = max(tmp_score, alpha)
                    if (best_move == None or tmp_score > best_score):
                        best_score = tmp_score
                        best_move = move
                    if(beta <= alpha):
                        best_score = tmp_score
                        break
            else:
                best_score = float("-inf")
                for move in legal_moves:
                    #find my score after the opponent moves
                    tmp_score = self.score(game.forecast_move(move), game.inactive_player)
                    beta = min(tmp_score, beta)
                    #keep the lowest score, because that is what the opponent will do
                    if (best_move == None or tmp_score < best_score):
                        best_score = tmp_score
                        best_move = move
                    if(beta <= alpha):
                        best_score = tmp_score
                        break
        return best_score, best_move