import time
import csv
import matplotlib.pyplot as plt
from Code.classes.VehicleClass import Vehicle
from Code.classes.RushClass import RushHour
from Code.algorithms.Random import *

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
    file = 'data/Rushhour9x9_6.csv'
    dimension = 9
    
    rush_game = load_file(file, dimension)
    solve_count = []
    
    num_runs = 100
    for _ in range(num_runs):
        
        count = solve_puzzle(rush_game)
        solve_count.append(count)
        
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f'Time: {total_time}')
    
    plt.hist(solve_count, bins=20, label=file)
    plt.show()


if __name__ == '__main__':
    main()


# if __name__ == '__main__':
#     filename = 'gameboards/Rushhour6x6_1.csv'
#     rushhour = load_file(filename)

#     results = breadth_first_search(rushhour, max_depth=10)

#     print(f'{0} Solutions found'.format(len(results['solutions'])))
#     for solution in results['solutions']:
#         print(f'Solution: {0}'.format(', '.join(solution_steps(solution))))

#     print(f'{0} Nodes visited'.format(len(results['visited'])))