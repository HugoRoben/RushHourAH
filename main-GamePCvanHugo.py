import time
import csv
import matplotlib.pyplot as plt
from Code.classes.VehicleClass import Vehicle
from Code.classes.RushClass import RushHour
from Code.algorithms.Random import *
from Code.algorithms.BFS import *


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

    file = 'data/Rushhour9x9_4.csv'
    dimension = 9

    rush_game = load_file(file, dimension)
    results = breadth_first_search(rush_game, max_depth=100)

    if results['solutions']:
        solution = results['solutions'][0]
        steps = solution_steps(solution)
        number_steps = len(solution)

        print(f'bord: {file}:')
        steps_output = ', '.join(f'{step}' for step in steps)
        print(f'Solved in {number_steps} steps: {steps_output}')

    else:
        print("No solution found")

    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f'Time taken: {time_taken:.2f} seconds')


if __name__ == "__main__":
    main()

    
    # solve_count = []
    
    # num_runs = 100
    # for _ in range(num_runs):
        
    #     count = solve_puzzle(rush_game)
    #     solve_count.append(count)
        
    # end_time = time.perf_counter()
    # total_time = end_time - start_time
    # print(f'Time: {total_time}')
    
    # plt.hist(solve_count, bins=20, label=file)
    # plt.show()



# def main():
#     start_time = time.perf_counter()

#     file = 'data/Rushhour6x6_2.csv'
#     dimension = 6

#     rush_game = load_file(file, dimension)
#     results = breadth_first_search(rush_game, max_depth=100)

#     if results['solutions']:
#         for i, solution in enumerate(results['solutions'], start=1):
#             steps = solution_steps(solution)
#             print(f'Solution {i}: {", ".join(steps)}')
#             print(f'Number of steps: {len(steps)}\n')
#     else:
#         print("No solution found")

#     end_time = time.perf_counter()
#     time_taken = end_time - start_time
#     print(f'Time taken: {time_taken:.2f} seconds')

# if __name__ == "__main__":
#     main()