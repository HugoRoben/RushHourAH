import time
import csv
import matplotlib.pyplot as plt
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

    # file = 'data/Rushhour9x9_4.csv'
    # dimension = 9
    file = 'data/Rushhour6x6_1.csv'
    dimension = 6

    start_state = load_file(file, dimension)
    goal_state = solve_puzzle(start_state)[0]
    results = astar_search(start_state, goal_state)
    if results is not None:
         print("something")
    # rush_game = load_file(file, dimension)
    # results = breadth_first_search(rush_game, max_depth=100)

    # if results['solutions']:
    #     solution = results['solutions'][0]
    #     steps = solution_steps(solution)
    #     number_steps = len(solution)

    #     print(f'bord: {file}:')
    #     steps_output = ', '.join(f'{step}' for step in steps)
    #     print(f'Solved in {number_steps} steps: {steps_output}')

    # else:
    #     print("No solution found")

    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f'Time taken: {time_taken:.2f} seconds')


if __name__ == "__main__":
    main()
