import random
from Code.visual.visualizer import *
from ..Classes.RushClass import RushHour


def random_solve_puzzle(Rush_game: RushHour, max_iterations: int=1000000):
    """
    Attempt to solve the Rush Hour puzzle using a random approach.

    Args:
    Rush_game (RushGame): An instance of the Rush Hour puzzle game.
    max_iterations (int): Maximum number of iterations to attempt for finding a solution.

    Returns:
    Optional[Dict[str, any]]: A dictionary containing the final game state and the solution path if solved, 
    otherwise None if no solution is found within the maximum iterations.
    """
    
    game = Rush_game
    solution_path = [game]

    for _ in range(max_iterations):
        if game.is_solved():
            # visualizer = Visualizer(600, 600)
            # visualizer.animate_solution(solution_path)
            return {'game': game, 'solution': solution_path}

        possible_moves = list(game.moves())
        if not possible_moves:
            break

        game = random.choice(possible_moves)
        solution_path.append(game)

    return None

