from Code.classes.VehicleClass import Vehicle

class RushHour(object):
    """A configuration of a single Rush Hour board."""

    def __init__(self, vehicles, dimension, move_count = 0, parent = None):
        self.vehicles = vehicles
        self.dim_board = dimension
        self.move_count = move_count
        self.parent = parent


    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if not isinstance(other, RushHour):
            return False
        return self.vehicles == other.vehicles and self.dim_board == other.dim_board

    def __ne__(self, other):
        return not self.__eq__(other)


    def __repr__(self):
        board = self.get_board()
        board_str = '-' * (self.dim_board + 2) + '\n'
        for row in board:
            board_str += '|' + ''.join(row) + '|\n'
        board_str += '-' * (self.dim_board + 2)
        return board_str


    def get_board(self):
        """Representation of the Rush Hour board as a 2D list of strings"""
        
        board = [[' ' for _ in range(self.dim_board)] for _ in range(self.dim_board)]

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
                    # yield RushHour(new_vehicles, self.dim_board)
                    yield RushHour(new_vehicles, self.dim_board, self.move_count + 1)

                if v.x + v.length < self.dim_board and board[v.y][v.x + v.length] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x + 1, v.y, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    # yield RushHour(new_vehicles, self.dim_board)
                    yield RushHour(new_vehicles, self.dim_board, self.move_count + 1)

            else:
                if v.y - 1 >= 0 and board[v.y - 1][v.x] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y - 1, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    # yield RushHour(new_vehicles, self.dim_board)
                    yield RushHour(new_vehicles, self.dim_board, self.move_count + 1)

                if v.y + v.length < self.dim_board and board[v.y + v.length][v.x] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y + 1, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    # yield RushHour(new_vehicles, self.dim_board)
                    yield RushHour(new_vehicles, self.dim_board, self.move_count + 1)

                    
    def is_solved(self):
        """Check if the puzzle is solved."""
        for vehicle in self.vehicles:
            if vehicle.id == 'X':
                return vehicle.x + vehicle.length == self.dim_board
        return False