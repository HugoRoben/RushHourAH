import argparse
import matplotlib.pyplot as plt
from Code.visual import results
from Code.algorithms.solvers import *

# python3 main.py txt bfs --game_range '0-2'
# python3 main.py txt bfs --single_game 1
# python3 main.py txt bfs --single_game 1 --repeat 2
# python3 main.py txt bfs --all_games
# python3 main.py txt bfs --single_game 1 --repeat 10
# python3 main.py txt bfs --all_games -- repeat 5
# python3 main.py csv bfs --dimension 6 --board 3
# python3 main.py csv bfs --dimension 6 --board 3 --repeat 5

import cProfile

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Rush Hour solver algorithms.")

    # Common parser arguments
    parser.add_argument("file_type", help="Type of file (csv or txt)", type=str)
    parser.add_argument("algorithm", help="Algorithm to use (Astar, IDDFS, BFS, Random)", type=str)
    parser.add_argument("--repeat", help="Number of times to repeat solving the same game", type=int, default=1)

    # Csv arguments
    parser.add_argument("--dimension", help="Dimension of the board (6, 9, or 12)", type=int)
    parser.add_argument("--board_number", help="Board number (1 to 7)", type=int)

    # TXT file specific arguments
    parser.add_argument("--single_game", help="Single game number to solve", type=int)
    parser.add_argument("--game_range", help="Range of games to solve, e.g., '0-2'", type=str)
    parser.add_argument("--all_games", help="Solve all games", action="store_true")
    return parser.parse_args()



def main():
    args = parse_arguments()
    rush_games = load_game_data(args)
    if not rush_games:
        return

    stats, unsolved_count, solutions = solve_rush_hour_games(rush_games, args.algorithm, args.repeat)

    if not stats["times"] or not stats["steps"]:
        print("No data for visualization available.")
        return

    results.visualize(stats, args.algorithm)
    results.desc_stats(stats, unsolved_count, args.algorithm)

    # for solution in solutions:
    #     visualizer = Visualizer(600, 600)
    #     visualizer.animate_solution(solution)
    
    if solutions:
        visualizer = Visualizer(600, 600)
        visualizer.animate_solution(solutions)


if __name__ == "__main__":
    main()