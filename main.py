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
from Code.algorithms.IDAstar import * 

# python3 main.py bfs --game_range '0-2'
# python3 main.py bfs --single_game 0

def parse_and_create_games(file_path, game_indices, dimension=6):
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i in game_indices:
                game_data = line.strip()
                steps, board_config, num_configs = game_data.split()
                vehicle_positions = {}

                for j, char in enumerate(board_config):
                    if char not in ['o', 'x']:  # vehicle found
                        if char not in vehicle_positions:
                            vehicle_positions[char] = [j]  # start position
                        else:
                            vehicle_positions[char].append(j)  # subsequent positions

                vehicles = []
                for vehicle_id, positions in vehicle_positions.items():
                    x, y = positions[0] % dimension, positions[0] // dimension
                    length = len(positions)
                    orientation = 'H' if positions[1] % dimension > positions[0] % dimension else 'V'

                    vehicles.append(Vehicle(vehicle_id, orientation, x, y, length))

                yield RushHour(set(vehicles), dimension)


# def main():
#     start_time = time.perf_counter()

#     parser = argparse.ArgumentParser(description="Run Rush Hour solver algorithms.")
#     parser.add_argument("algorithm", help="Algorithm to use (Astar, IDDFS, BFS)", type=str)
#     parser.add_argument("--single_game", help="Single game number to solve", type=int)
#     parser.add_argument("--game_range", help="Range of games to solve, e.g., '500-1000'", type=str)
  
#     args = parser.parse_args()

#     file = 'data/no_wall_rush.txt'
#     if args.single_game is not None:
#         game_indices = [args.single_game]
#     elif args.game_range is not None:
#         start, end = map(int, args.game_range.split('-'))
#         game_indices = list(range(start, end + 1))
#     else:
#         print("Please specify either --single_game or --game_range")
#         return

#     rush_games = parse_and_create_games(file, game_indices)
#     # print(rush_games)
    
#     for rush_game in rush_games:
#         if args.algorithm.lower() == 'astar':
#             results = Astar(rush_game).astar_search_single_ended(rush_game)
#             if results is not None:
#                 print(f'Board: {file}:')
#                 print(results)
    
#         elif args.algorithm.lower() == 'idastar':
#             ida_star_solver = IDAstar(rush_game)
#             results = ida_star_solver.idastar_search(rush_game)
#             if results is not None:
#                 print(f'Board: {file}:')
#                 print(f'Solved in {results} iterations')
#             else:
#                 print("No solution found")

#         elif args.algorithm.lower() == 'iddfs':
#             results = iterative_deepening_search(rush_game, max_depth=500)
#             if results['solutions']:
#                 solution = results['solutions'][0]
#                 steps = solution_steps(solution)
#                 number_steps = len(solution)
#                 print(f'Board: {file}:')
#                 steps_output = ', '.join(f'{step}' for step in steps)
#                 print(f'Solved in {number_steps} steps: {steps_output}')
#             else:
#                 print("No solution found")

#         elif args.algorithm.lower() == 'bfs':
#             results = breadth_first_search(rush_game, max_depth=500)
#             if results['solutions']:
#                 solution = results['solutions'][0]
#                 steps = solution_steps(solution)
#                 number_steps = len(steps)
#                 # print(f'Board: {file}:')
#                 # steps_output = ', '.join(f'{step}' for step in steps)
#                 # print(f'Solved in {number_steps} steps: {steps_output}')
#                 print(f'Solved in {number_steps} steps')
#             else:
#                 print("No solution found")

#         else:
#             print("Invalid algorithm. Please choose from Astar, IDDFS, or BFS.")

#     end_time = time.perf_counter()
#     time_taken = end_time - start_time
#     print(f'Time taken: {time_taken:.2f} seconds')


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
    
    elif args.algorithm.lower() == 'idastar':
        ida_star_solver = IDAstar(rush_game)
        results = ida_star_solver.idastar_search(rush_game)
        if results is not None:
            print(f'Board: {file}:')
            print(f'Solved in {results} iterations')
        else:
            print("No solution found")

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
