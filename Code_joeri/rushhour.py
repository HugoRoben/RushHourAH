from vehicle import Vehicle
import csv
import random

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
    dimension_board = 6
    with open(rushhour_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                id, orientation, x, y, length = row
                vehicles.append(Vehicle(id, orientation, int(x) - 1, int(y) - 1, int(length)))
            return RushHour(set(vehicles), dimension_board)



# def extract_dimension(filename):
#     part = filename.split('/')[-1]
#     dimension = part.split('x')[0]
#     return int(dimension)



if __name__ == '__main__':
    filename = "gameboards/Rushhour6x6_3.csv"
    rushhour_initial = load_file(filename)
    rushhour_current = rushhour_initial

    move_count = 0
    while not rushhour_current.is_solved():
        next_state = rushhour_current.make_random_move()
        if next_state is None:
            print("No more moves available.")
            break
        rushhour_current = next_state
        move_count += 1
        print(rushhour_current) 

    print(f"Solved in {move_count} steps with random moves.")

