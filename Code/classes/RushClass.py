from Code.classes.VehicleClass import Vehicle

class RushHour(object):
    def __init__(self, vehicles, dimension, move_count = 0, parent = None):
        self.vehicles = vehicles
        self.dim_board = dimension
        self.move_count = move_count
        self.parent = parent
        self.vehicle_history = {v.id: [] for v in vehicles}

    def update_history(self):
        """ keep track of movement history for oscillation patterns in A* algo"""
        for v in self.vehicles:
            self.vehicle_history[v.id].append((v.x, v.y))

    def __hash__(self):
        return hash(self.__repr__())


    def __eq__(self, other):
        return hash(self) == hash(other)

    # def __eq__(self, other):
    #     if not isinstance(other, RushHour):
    #         return False
    #     return self.vehicles == other.vehicles

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
                    board[y][x+i] = vehicle.id
            else:
                for i in range(vehicle.length):
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
                    yield RushHour(new_vehicles, self.dim_board, parent = self)

                if v.x + v.length < self.dim_board and board[v.y][v.x + v.length] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x + 1, v.y, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles, self.dim_board, parent = self)

            else:
                if v.y - 1 >= 0 and board[v.y - 1][v.x] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y - 1, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles, self.dim_board, parent = self)

                if v.y + v.length < self.dim_board and board[v.y + v.length][v.x] == ' ':
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y + 1, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield RushHour(new_vehicles, self.dim_board, parent = self)

    def generate_future_states(self, current_state, depth=5):
        if depth == 0:
            return [current_state]

        future_states = []
        for next_state in current_state.moves():
            future_states.extend(self.generate_future_states(next_state, depth - 1))

        return future_states
                    
    def is_solved(self):
        """Check if the puzzle is solved."""
        for vehicle in self.vehicles:
            if vehicle.id == 'X':
                return vehicle.x + vehicle.length == self.dim_board
        return False