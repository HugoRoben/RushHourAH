'''
Class representing a game of rush hour. The class includes a 2D representation
of the board in a state, generates all possible moves in a state, and checks
if a game is won.
'''

from Code.classes.VehicleClass import Vehicle

class RushHour(object):
    """A configuration of a single Rush Hour board."""

    def __init__(self, vehicles, dimension, parent = None, occupied_coords = None):
        self.vehicles = vehicles
        self.dim_board = dimension
        self.parent = parent
        # get occupied coordinates from vehicles if first initialisation of the game
        if occupied_coords == None:
            self.occupied_coords = self.get_occupied_coords_set()
        else: 
            self.occupied_coords = occupied_coords

    def get_occupied_coords_set(self):
        '''Adds tuples: (x,y) for the occupied coordinates in the begin state of the game'''
        coords = set()
        for v in self.vehicles:
            for i in range(v.length):
                coords.add((v.x + i, v.y) if v.orientation == 'H' else (v.x, v.y + i))
        return coords
    
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
        # start with an empty board
        board = [[' ' for _ in range(self.dim_board)] for _ in range(self.dim_board)]
        # add the id of the vehicles to the board on the corresponding tiles
        for vehicle in self.vehicles:
            for i in range(vehicle.length):
                coord = (vehicle.x + i, vehicle.y) if vehicle.orientation == 'H' else (vehicle.x, vehicle.y + i)
                board[coord[1]][coord[0]] = vehicle.id
        return board

    def moves(self):
        """Return iterator of next possible moves."""
        for v in self.vehicles:
            # horziontal moves
            if v.orientation == 'H':
                # check if tile next to vehicle is free
                if v.x - 1 >= 0 and (v.x - 1, v.y) not in self.occupied_coords:
                    new_v = Vehicle(v.id, v.orientation, v.x - 1, v.y, v.length)
                    # copy vehicles, remove old vehicle and add vehicle with new coordinates
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    # copy set with coordinates, remove old coordinate add new coordinate after move
                    new_occupied_coords = self.occupied_coords.copy()
                    new_occupied_coords.remove((v.x + v.length - 1, v.y))
                    new_occupied_coords.add((v.x - 1, v.y))
                    # yield new rush hour game
                    yield RushHour(new_vehicles, self.dim_board, parent = self, occupied_coords = new_occupied_coords)
                if v.x + v.length < self.dim_board and (v.x + v.length, v.y) not in self.occupied_coords:
                    new_v = Vehicle(v.id, v.orientation, v.x + 1, v.y, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    new_occupied_coords = self.occupied_coords.copy()
                    new_occupied_coords.remove((v.x, v.y))
                    new_occupied_coords.add((v.x + v.length, v.y))
                    yield RushHour(new_vehicles, self.dim_board, parent=self, occupied_coords=new_occupied_coords)
                    
            # vertical moves
            else: 
                if v.y - 1 >= 0 and (v.x, v.y - 1) not in self.occupied_coords:
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y - 1, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    new_occupied_coords = self.occupied_coords.copy()
                    new_occupied_coords.remove((v.x, v.y + v.length - 1))
                    new_occupied_coords.add((v.x, v.y - 1))
                    yield RushHour(new_vehicles, self.dim_board, parent=self, occupied_coords=new_occupied_coords)
                if v.y + v.length < self.dim_board and (v.x, v.y + v.length) not in self.occupied_coords:
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y + 1, v.length)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    new_occupied_coords = self.occupied_coords.copy()
                    new_occupied_coords.remove((v.x, v.y))
                    new_occupied_coords.add((v.x, v.y + v.length))
                    yield RushHour(new_vehicles, self.dim_board, parent=self, occupied_coords=new_occupied_coords)

    def generate_future_states(self, current_state, depth=3):
        '''Allows to look a specified amount of states ahead from a certain state'''
        # if depth is 0, no look ahead is required
        if depth == 0:
            return [current_state]
        # generate every future state from current state and add to a list
        # up to a certain depth
        future_states = []
        for next_state in current_state.moves():
            future_states.extend(self.generate_future_states(next_state, depth - 1))
        return future_states
    
    def is_solved(self):
        """Check if the puzzle is solved."""
        for vehicle in self.vehicles:
            if vehicle.id == 'X':
                # check if red car is at the exit
                return vehicle.x + vehicle.length == self.dim_board
        return False
    
