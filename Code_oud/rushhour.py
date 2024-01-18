from vehicle import Vehicle
import csv
import random
import glob
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class RushHour(object):
    """A configuration of a single Rush Hour board."""

    def __init__(self, vehicles, dim_board):
        self.vehicles = vehicles
        self.dim_board = dim_board


    def __hash__(self):
        return hash(self.__repr__())


    def __eq__(self, other):
        return self.vehicles == other.vehicles


    def __ne__(self, other):
        return not self.__eq__(other)


    def __repr__(self):
        s = '-' * (self.dim_board + 2) + '\n'
        for line in self.get_board():
            s += '|{0}|\n'.format(''.join(line))
        s += '-' * (self.dim_board + 2) + '\n'
        return s


    def get_board(self):
        """Representation of the Rush Hour board as a 2D list of strings"""
        
        board = [[' ' for _ in range(self.dim_board)] for _ in range(self.dim_board)]
        
        # board = [[' ', ' ', ' ', ' ', ' ', ' '],
        #          [' ', ' ', ' ', ' ', ' ', ' '],
        #          [' ', ' ', ' ', ' ', ' ', ' '],
        #          [' ', ' ', ' ', ' ', ' ', ' '],
        #          [' ', ' ', ' ', ' ', ' ', ' '],
        #          [' ', ' ', ' ', ' ', ' ', ' ']]

        for vehicle in self.vehicles:
            x, y = vehicle.x, vehicle.y
            if vehicle.orientation == 'H':
                for i in range(vehicle.length):
                    # print(f"Placing vehicle {vehicle.id} at: ({y}, {x+i})")  # Debug print
                    board[y][x+i] = vehicle.id
            else:
                for i in range(vehicle.length):
                    # print(f"Placing vehicle {vehicle.id} at: ({y+i}, {x})")  # Debug print
                    board[y+i][x] = vehicle.id

        return board


    def moves(self):
        """Return iterator of next possible moves."""
        board = self.get_board()
        for v in self.vehicles:
            if v.orientation == 'H':
                if v.x - 1 >= 0 and board[v.y][v.x - 1] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x - 1, v.y, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles, self.dim_board)
                if v.x + v.length < self.dim_board and board[v.y][v.x + v.length] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x + 1, v.y, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles, self.dim_board)
            else:
                if v.y - 1 >= 0 and board[v.y - 1][v.x] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y - 1, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles, self.dim_board)
                if v.y + v.length < self.dim_board and board[v.y + v.length][v.x] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y + 1, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles, self.dim_board)
                    
    def is_solved(self):
        """Check if the puzzle is solved."""
        for vehicle in self.vehicles:
            if vehicle.id == 'X':  # Assuming 'X' is the goal vehicle
                return vehicle.x + vehicle.length == self.dim_board
        return False



def load_file(rushhour_file):
    vehicles = []
    dim_board = extract_dimension(rushhour_file)
    with open(rushhour_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                id, orientation, x, y, length = row
                vehicles.append(Vehicle(id, orientation, int(x) - 1, int(y) - 1, int(length)))
            return RushHour(set(vehicles), dim_board)



def extract_dimension(filename):
    gameboard_name = os.path.basename(filename).split('.')[0]
    size_part = gameboard_name.split('_')[0]
    dim_board = int(size_part.replace('Rushhour', '').split('x')[0])
    return int(dim_board)


class RushHourSolver:
    def __init__(self, rush_hour_game):
        self.game = rush_hour_game
        # self.visited_states = set()
        self.move_count = 0

    def make_random_move(self):
        possible_moves = list(self.game.moves())
        if not possible_moves:
            return None
        return random.choice(possible_moves)

    def solve_puzzle(self, max_iterations=1000000):
        for _ in range(max_iterations):
            if self.game.is_solved():
                return self.move_count

            next_state = self.make_random_move()
            if next_state is None:  # or hash(next_state) in self.visited_states
                print("No more moves available or state repeated.")
                break

            # self.visited_states.add(hash(next_state))
            self.move_count += 1
            self.game = next_state  # Update the game state

        return 0


def calculate_statistics(times, move_counts):
    avg_time = sum(times) / len(times)
    avg_moves = sum(move_counts) / len(move_counts)
    max_time = max(times)
    min_time = min(times)
    max_moves = max(move_counts)
    min_moves = min(move_counts)

    return {
        "average_time": avg_time,
        "average_moves": avg_moves,
        "max_time": max_time,
        "min_time": min_time,
        "max_moves": max_moves,
        "min_moves": min_moves
    }


def plot_combined_statistics(file_stats):
    all_times = []
    all_moves = []
    labels = []

    for file, stats in file_stats.items():
        all_times.extend(stats["times"])
        all_moves.extend(stats["moves"])
        labels.extend([os.path.basename(file)] * len(stats["times"]))

    data = pd.DataFrame({
        'Time': all_times,
        'Moves': all_moves,
        'File': labels
    })

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    sns.boxplot(x='File', y='Time', data=data)
    plt.xticks(rotation=45)
    plt.title("Time Taken for Each File")
    plt.ylabel("Time (seconds)")

    plt.subplot(1, 2, 2)
    sns.boxplot(x='File', y='Moves', data=data)
    plt.xticks(rotation=45)
    plt.title("Move Counts for Each File")
    plt.ylabel("Number of Moves")

    plt.tight_layout()
    plt.show()


def main():
    file = 'gameboards/Rushhour9x9_6.csv'
    start_time = time.perf_counter()

    rush_game = load_file(file)
    solver = RushHourSolver(rush_game)
    move_count = solver.solve_puzzle()

    end_time = time.perf_counter()
    total_time = end_time - start_time

    times = [total_time]
    move_counts = [move_count]

    stats = calculate_statistics(times, move_counts)
    stats["file"] = os.path.basename(file)

    stats_df = pd.DataFrame([stats])
    print(stats_df)


if __name__ == '__main__':
    main()


# def main():
#     num_runs = 3
#     solutions_dict = {}
#     all_stats = []

#     for file in glob.glob('gameboards/*.csv'):
#         times = []
#         move_counts = []

#         for _ in range(num_runs):
#             start_time = time.perf_counter()

#             rush_game = load_file(file)
#             solver = RushHourSolver(rush_game)
#             move_count = solver.solve_puzzle()

#             end_time = time.perf_counter()
#             total_time = end_time - start_time

#             times.append(total_time)
#             move_counts.append(move_count)

#         stats = calculate_statistics(times, move_counts)
#         stats_for_plot = stats.copy()
#         stats_for_plot["times"] = times
#         stats_for_plot["moves"] = move_counts
#         solutions_dict[file] = stats_for_plot

#         stats["file"] = os.path.basename(file)
#         all_stats.append(stats)

#     stats_df = pd.DataFrame(all_stats)
#     print(stats_df)

#     plot_combined_statistics(solutions_dict)


# if __name__ == '__main__':
#     main()
