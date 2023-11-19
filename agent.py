"""
An AI player for Othello. 
"""

import random
import sys
import time

"""
Heuristic , on a given board an interesting way of conputing a heuristic would be to calculate how many 
lines would be captured for each moves .  for each player given us an idea of the contol that each player have of a position, 
according to the link on the assignement page haing corners is good so if any move is in a corner of the table this would make te move worth
more important hence i decided to make it +5 (so that it is powerfull but would not have a terrible weight either .)
So a position is good if you can transorm a lot from your opponent calculated by lines and if you can control a lot of corners compared to your
opponent.



"""
# You can use the functions from othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache = {} # Use this for state caching

def eprint(*args, **kwargs): #use this for debugging, to print to sterr
    print(*args, file=sys.stderr, **kwargs)
    
def compute_utility(board, color):
    # IMPLEMENT!
    """
    Method to compute the utility value of board.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents utility
    """
    scores = get_score(board)
    if color == 1:
        return  scores[0] - scores[1]
      
    return  scores[1] - scores[0]
    

def compute_heuristic(board, color):
    # IMPLEMENT! Optional though!
    """
    Method to heuristic value of board, to be used if we are at a depth limit.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents heuristic value
    """
    sum1 = 0
    sum2 = 0
    if color == 1: next = 2
    else: next = 1
    allowed_moves1 = get_possible_moves(board, color)
    allowed_moves2 = get_possible_moves(board, next)
    for mov in allowed_moves1:
        lines = find_lines(board, mov[0], mov[1],color)
        for line in lines:
            for point in line:
                sum1 +=1 
        if mov[0] == len(board[0])-1 or mov[1] == len(board[0])-1 or mov[0] == 0 or mov[1] == 0:
            sum1+=4
    for mov in allowed_moves2:
        lines = find_lines(board, mov[0], mov[1],color)
        for line in lines:
            for point in line:
                sum2 +=1 
        if mov[0] == len(board[0])-1 or mov[1] == len(board[0])-1 or mov[0] == 0 or mov[1] == 0:
            sum2+=4
    return sum1 - sum2
    

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    A helper function for minimax that finds the lowest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the max utiltiy
    # 4. After checking every move, you can find the minimum utility
    # ...
    fin_util = 100000000
    if color == 1: next = 2
    else: next = 1
    if limit == 0 :
         return (None, compute_utility(board, color))
    if caching == 1 and board in cache:
        return cache[board]
    allowed_moves = get_possible_moves(board, next)
    if len(allowed_moves) == 0  :
        return (None, compute_utility(board, color))
    for allowed in allowed_moves:
        new_board = play_move(board, next, allowed[0], allowed[1])
        mov , util = minimax_max_node(new_board, color, limit -1 , caching)
        if caching ==1:
                cache[new_board] = ( mov , util)
        if util < fin_util:
            fin_util = util
            fin_move = allowed

    return (fin_move, fin_util)
    


def minimax_max_node(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    A helper function for minimax that finds the highest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the min utiltiy
    # 4. After checking every move, you can find the maximum utility
    # ...
    fin_util = -100000000
    if limit == 0 :
         return (None, compute_utility(board, color))
    if caching == 1 and board in cache:
        return cache[board]
    allowed_moves = get_possible_moves(board, color)
    if len(allowed_moves) == 0  :
        return (None, compute_utility(board, color))
    for  allowed in allowed_moves:
        new_board = play_move(board, color, allowed[0], allowed[1])
        mov, util= minimax_min_node(new_board, color, limit - 1, caching)
        if caching ==1:
            cache[new_board] = ( mov , util)
        if util > fin_util:
            fin_util = util
            fin_move = allowed
    return (fin_move, fin_util)

    
def select_move_minimax(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Minimax algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    INPUT: a game state, the player that is in control, the depth limit for the search, and a flag determining whether state caching is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """
    cache.clear()
    return minimax_max_node(board, color, limit, caching)[0]


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    A helper function for alpha-beta that finds the lowest possible utility (don't forget to utilize and update alpha and beta!)
    """
    
    fin_util = 100000000
    if color == 1: next = 2
    else: next = 1
    if caching == 1 and board in cache:
        return cache[board]
    if limit == 0 :
         return (None, compute_utility(board, color)) 
    allowed_moves = get_possible_moves(board, next)
    if ordering == 1 :
        allowed_moves.sort(key=lambda coord: compute_utility(play_move(board, color, coord[0], coord[1]), color) )
    if len(allowed_moves) == 0  :
        return (None, compute_utility(board, color))
    for allowed in allowed_moves:
        new_board = play_move(board, next, allowed[0], allowed[1])

        mov, util = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        if caching ==1:
            cache[new_board] = ( mov , util)
        if util < fin_util:
            fin_util = util
            fin_move = allowed
        if fin_util < beta :
            beta = fin_util
        if beta <= alpha:
            return   (fin_move, fin_util)

    return (fin_move, fin_util)

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    A helper function for alpha-beta that finds the highest possible utility (don't forget to utilize and update alpha and beta!)
    """
    fin_util = -100000000
    if caching == 1 and board in cache:
        return cache[board]
    if limit == 0 :
         return (None, compute_utility(board, color))
    
    allowed_moves = get_possible_moves(board, color)
    if ordering == 1 :
        allowed_moves.sort(key=lambda coord: compute_utility(play_move(board, color, coord[0], coord[1]), color) , reverse=True)
    if len(allowed_moves) == 0  :
        return (None, compute_utility(board, color))
    for allowed in allowed_moves:
        new_board = play_move(board, color, allowed[0], allowed[1])
        mov, util = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching , ordering)
        if caching ==1:
            cache[new_board] = ( mov , util)
        if util > fin_util:
            fin_util = util
            fin_move = allowed
        if fin_util > alpha :
            alpha = fin_util
        if beta <= alpha:
            return   (fin_move, fin_util)

    return (fin_move, fin_util)

def select_move_alphabeta(board, color, limit = -1, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Alpha-Beta algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    INPUT: a game state, the player that is in control, the depth limit for the search, a flag determining whether state caching is on or not, a flag determining whether node ordering is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """
    cache.clear()
    return alphabeta_max_node(board, color, -1000000 ,1000000, limit , caching, ordering)[0]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) # Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) # Depth limit
    minimax = int(arguments[2]) # Minimax or alpha beta
    caching = int(arguments[3]) # Caching 
    ordering = int(arguments[4]) # Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): # run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: # else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
