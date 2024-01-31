import random
from Code.visual.visualizer import *
from ..classes.RushClass import RushHour
from typing import Union, Dict, List, Optional


def random_solve_puzzle(Rush_game: RushHour, max_iterations: int=1000000)\
    -> Optional[Dict[str, Union[int, List[RushHour], Dict[int, List[RushHour]]]]]:
    """
    Attempt to solve the Rush Hour puzzle using a random approach.

    Args:
    ---------------------------------------------------------------------------
        Rush_game (RushGame): An instance of the Rush Hour puzzle game.
        max_iterations (int): Maximum number of iterations to attempt for 
        finding a solution.

    Returns:
    ---------------------------------------------------------------------------
        Optional[Dict[str, Union[int, List[RushHour], Dict[int, List[RushHour]]]]]:
        A dictionary containing the final game state and the solution path if 
        solved, otherwise None if no solution is found within the maximum iterations.
    """
    
    game = Rush_game
    solution_path = [game]

    for _ in range(max_iterations):
        if game.is_solved():
            return {'game': game, 'solution': solution_path, 'visited': _}

        possible_moves = list(game.moves())
        # break if no more possible moves
        if not possible_moves:
            break
        # choose a random new state from the list to make move
        game = random.choice(possible_moves)
        solution_path.append(game)

    return None

