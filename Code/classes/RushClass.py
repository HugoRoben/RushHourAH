from Code.classes.VehicleClass import Vehicle

class RushHour(object):
    """A configuration of a single Rush Hour board."""

    def __init__(self, vehicles, dimension):
        self.vehicles = vehicles
        self.dim_board = dimension


    def __hash__(self):
        return hash(self.__repr__())


    def __eq__(self, other):
        return self.vehicles == other.vehicles


    def __ne__(self, other):
        return not self.__eq__(other)


    def __repr__(self):
        s = '-' * 8 + '\n'
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