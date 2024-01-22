import time
import csv
import argparse
import matplotlib.pyplot as plt
from Code.algorithms.IDDFS import *
from Code.classes.VehicleClass import Vehicle
from Code.classes.RushClass import RushHour
from Code.algorithms.Random import *
from Code.algorithms.BFS import *
from Code.algorithms.Astar import * 


def load_file(rushhour_file, dimension):
    vehicles = []
    dim_board = dimension
    with open(rushhour_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                id, orientation, x, y, length = row
                vehicles.append(Vehicle(id, orientation, int(x) - 1, int(y) - 1, int(length)))
            return RushHour(set(vehicles), dim_board)


def main():
    start_time = time.perf_counter()

    parser = argparse.ArgumentParser(description="Run Rush Hour solver algorithms.")
    parser.add_argument("algorithm", help="Algorithm to use (Astar, IDDFS, BFS)", type=str)
    parser.add_argument("dimension", help="Dimension of the board (6, 9, or 12)", type=int)
    parser.add_argument("board_number", help="Board number (1 to 7)", type=int)
    args = parser.parse_args()

    file = f'data/Rushhour{args.dimension}x{args.dimension}_{args.board_number}.csv'
    dimension = args.dimension
    rush_game = load_file(file, dimension)
    
    if args.algorithm.lower() == 'astar':
        results = Astar(rush_game).astar_search_single_ended(rush_game)
        if results is not None:
            print(f'Board: {file}:')
            print(results)

    elif args.algorithm.lower() == 'iddfs':
        results = iterative_deepening_search(rush_game, max_depth=500)
        if results['solutions']:
            solution = results['solutions'][0]
            steps = solution_steps(solution)
            number_steps = len(solution)
            print(f'Board: {file}:')
            steps_output = ', '.join(f'{step}' for step in steps)
            print(f'Solved in {number_steps} steps: {steps_output}')
        else:
            print("No solution found")

    elif args.algorithm.lower() == 'bfs':
        results = breadth_first_search(rush_game, max_depth=500)
        if results['solutions']:
            solution = results['solutions'][0]
            steps = solution_steps(solution)
            number_steps = len(solution)
            print(f'Board: {file}:')
            steps_output = ', '.join(f'{step}' for step in steps)
            print(f'Solved in {number_steps} steps: {steps_output}')
        else:
            print("No solution found")

    else:
        print("Invalid algorithm. Please choose from Astar, IDDFS, or BFS.")

    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f'Time taken: {time_taken:.2f} seconds')

if __name__ == "__main__":
    main()
