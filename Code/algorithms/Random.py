import random
from Code.visual.visualizer import *


def random_solve_puzzle(Rush_game, max_iterations=1000000):
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

