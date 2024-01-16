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

    def is_solved(self):
        """Check if the puzzle is solved."""
        for vehicle in self.vehicles:
            if vehicle.id == 'X':  # Assuming 'X' is the goal vehicle
                return vehicle.x + vehicle.length == self.dim_board
        return False


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

    def make_random_move(self):
        possible_moves = list(self.moves()) 
        if not possible_moves:
            return None
        return random.choice(possible_moves)


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


def solve():
    solutions_dict = {}
    start_time = time.time()
    for file in glob.glob('gameboards/*.csv'):
        game_name = os.path.basename(file).split('.')[0]
        rushhour_initial = load_file(file)
        
        number_of_steps = []

        for _ in range(2): 
            rushhour_current = rushhour_initial
            
            move_count = 0
            while not rushhour_current.is_solved():
                next_state = rushhour_current.make_random_move()
                if next_state is None:
                    print("No more moves available.")
                    break
                rushhour_current = next_state
                move_count += 1
                # print(rushhour_current) 
            number_of_steps.append(move_count)
            #print(f"Solved in {move_count} steps with random moves.")
            
        solutions_dict[game_name] = number_of_steps
        print(solutions_dict[game_name])
        
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time} seconds")
    return solutions_dict


def plot(solutions_dict):
    gameboards = []
    steps = []
    
    for gameboard, step_counts in solutions_dict.items():
        gameboards.extend([gameboard] * len(step_counts))
        steps.extend(step_counts)

    # Create a dataframe
    data = pd.DataFrame({'Gameboard': gameboards, 'Steps': steps})

    # Create a boxplot
    plt.figure(figsize=(12, 8))

    # Boxplot
    sns.boxplot(data=data, x='Gameboard', y='Steps', palette="Set2")

    # Adding scatterplot
    sns.stripplot(data=data, x='Gameboard', y='Steps', color='black', alpha=0.5, jitter=True)

    # Customizing plot
    plt.xlabel('Gameboard')
    plt.ylabel('Number of Steps')
    plt.title('Boxplot and Scatterplot of Steps to Solve Rush Hour Puzzles per Gameboard')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.show()


    stats_data = []
    for gameboard, steps in solutions_dict.items():
        gameboard_data = pd.Series(steps)
        stats = {
            'Gameboard': gameboard,
            'Mean': gameboard_data.mean(),
            'Median': gameboard_data.median(),
            'Min': gameboard_data.min(),
            'Max': gameboard_data.max(),
            'Std': gameboard_data.std()
        }
        stats_data.append(stats)

    descriptive_stats_df = pd.DataFrame(stats_data)

    print(descriptive_stats_df)
    # descriptive_stats_df.to_csv('gameboard_statistics.csv', index=False)

if __name__ == '__main__':
    solution = solve()
    plot(solution)