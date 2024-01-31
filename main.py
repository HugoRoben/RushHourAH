from argparse import Namespace, ArgumentParser
from Code.visual import results
from Code.algorithms.solvers import load_game_data, solve_rush_hour_games
from Code.visual.visualizer import Visualizer

def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Run Rush Hour solver algorithms.")

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
    
    if args.algorithm == 'random':
        results.plot_steps_histogram(stats['steps'], args.algorithm)
    
    if solutions:
        visualizer = Visualizer(600, 600)
        visualizer.animate_solution(solutions)


if __name__ == "__main__":
    main()