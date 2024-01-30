'''
Class representing a game of rush hour. The class includes a 2D representation
of the board in a state, generates all possible moves in a state, and checks
if a game is won.
'''
from Code.classes.VehicleClass import Vehicle
from typing import Tuple, Set, Optional, List
from bisect import insort

class RushHour(object):
    """A configuration of a single Rush Hour board."""

    def __init__(self, vehicles: set, dimension: int, parent: 'RushHour' = None, occupied_coords: set = None):
        # self.vehicles = vehicles
        self.vehicles = sorted(vehicles, key=lambda v: v.id)
        self.dim_board = dimension
        self.parent = parent
        self.red_car = self.get_red_car()
        self.blockers = self.get_cars_blocking_red()
        # get occupied coordinates from vehicles if first initialisation of the game
        if occupied_coords == None:
            self.occupied_coords = self.get_occupied_coords_set()
        else: 
            self.occupied_coords = occupied_coords

    def get_vehicle_coords(self, vehicle: Vehicle) -> Tuple[str, str]:
        return {(vehicle.x + i, vehicle.y) if vehicle.orientation == 'H'\
                else (vehicle.x, vehicle.y + i) 
            for i in range(vehicle.length)}

    def get_occupied_coords_set(self) -> Set[Tuple]:
        return set().union(*map(self.get_vehicle_coords, self.vehicles))
    
    def __eq__(self, other: 'RushHour'):
        if not isinstance(other, RushHour):
            return False
        return self.vehicles == other.vehicles

    def __ne__(self, other: 'RushHour'):
        return not self.__eq__(other)

    def __hash__(self):
        board_str = ''.join(f'{v.id}{v.x}{v.y}' for v in self.vehicles)
        return hash(board_str)

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
    
    def get_red_car(self) -> Optional[Vehicle]:
        """
        Get the red car from the dictionary of vehicles in a state.

        Returns:
        -----------------------------------------------------------------------
            Optional[Vehicle]: The red car Vehicle object if found,
            None otherwise.
        """
        for vehicle in self.vehicles:
            if vehicle.id == 'X':
                red_car = vehicle
                return red_car
        # return None if red car not found
        return None
    
    def get_cars_blocking_red(self) -> List[Vehicle]:
        """
        Get the cars blocking the 'X' car (red car).

        Returns:
        -----------------------------------------------------------------------
            List[Vehicle]: A list of vehicles that are blocking the red car.
        """
        # get teh red car
        red_car = self.red_car
        blocking_cars = []
        # iterate through vehicle set and add blocking vehicles to the list
        for v in self.vehicles:
            # horizontal cars can not block the red car
            if v.x > red_car.x + 1 and v.orientation == 'V':
                if v.y == red_car.y - 1 or v.y == red_car.y or\
                        (v.y == red_car.y - 2 and v.length == 3):
                    blocking_cars.append(v)
        return blocking_cars

    def moves(self):
        """Return iterator of next possible moves."""
        for v in self.vehicles:
            # horziontal moves
            if v.orientation == 'H':
                # check if tile next to vehicle is free
                if self.is_valid_move(v, 'left'):
                    # create new vehicle with new coordinates
                    new_v = Vehicle(v.id, v.orientation, v.x - 1, v.y, v.length)
                    new_coords = (v.x - 1, v.y)
                    # yield the new state of the game with updated vehicle position
                    yield from self.perform_move(v, new_v, (v.x + v.length - 1, v.y), new_coords)
                if self.is_valid_move(v, 'right'):
                    new_v = Vehicle(v.id, v.orientation, v.x + 1, v.y, v.length)
                    new_coords = (v.x + v.length, v.y)
                    yield from self.perform_move(v, new_v, (v.x, v.y), new_coords)
            # vertical moves
            else: 
                if self.is_valid_move(v, 'down'):
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y - 1, v.length)
                    new_coords = (v.x, v.y - 1)
                    yield from self.perform_move(v, new_v, (v.x, v.y + v.length - 1), new_coords)
                if self.is_valid_move(v, 'up'):
                    new_v = Vehicle(v.id, v.orientation, v.x, v.y + 1, v.length)
                    new_coords = (v.x, v.y + v.length)
                    yield from self.perform_move(v, new_v, (v.x, v.y), new_coords)
    
    def is_valid_move(self, v: Vehicle, direction: str):
        '''Checks if move is valid given Vehicle and direction'''
        # check horizontal moves
        if v.orientation == 'H':
            if direction == 'left':
                return v.x - 1 >= 0 and (v.x - 1, v.y) not in self.occupied_coords
            if direction == 'right':
                return v.x + v.length < self.dim_board and (v.x + v.length, v.y) not in self.occupied_coords
        # check vertical moves
        if v.orientation == 'V':
            if direction == 'up':
                return v.y + v.length < self.dim_board and (v.x, v.y + v.length) not in self.occupied_coords
            if direction == 'down':
                return v.y - 1 >= 0 and (v.x, v.y - 1) not in self.occupied_coords

    def perform_move(self, v: Vehicle, new_v: Vehicle, old_coords: tuple, new_coords: tuple):
        '''Performs moves by yielding new states of the game'''
        # copy existing vehicles set
        new_vehicles = self.vehicles.copy()
        # remove vehicle to be moved and add back with updated coordinates
        new_vehicles.remove(v)
        # new_vehicles.add(new_v)
        insort(new_vehicles, new_v)
        # copy and update the set of te occupied coordinates
        new_occupied_coords = self.occupied_coords.copy()
        new_occupied_coords.remove(old_coords)
        new_occupied_coords.add(new_coords)
        # yield the new state
        yield RushHour(new_vehicles, self.dim_board, parent=self, occupied_coords=new_occupied_coords)

    def generate_future_states(self, current_state: 'RushHour', depth=3):
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
    
    def is_solvable(self) -> bool:
        """
        Checks if there is only one blocking car left which can be moved to
        solve the board. The function checks if in the last column of the board
        there is only one car, of length 3, left which can be moved far enough
        up or down to free the path to the exit.

        Returns:
        -----------------------------------------------------------------------
            bool: True if the game is solvable, False otherwise.
        """
       
        # for 9x9 and 12x12 boards
        # check if the blocking car is in a position it can move
        # out of the free the exit
        # without having to move other vehicles
        if(self.dim_board // 2 == 0): exit_row = self.dim_board // 2 - 1
        else: exit_row = self.dim_board // 2
        
        if self.dim_board == 9 or self.dim_board == 12:
            for blocker in self.blockers:
                if blocker.length == 3:
                    if blocker.y == exit_row - 2:
                        coords_up = {(blocker.x, blocker.y - 1)}
                        coords_down = {(blocker.x, blocker.y + i) for i in range(3, 6)}

                    elif blocker.y == exit_row - 1:
                        coords_up = {(blocker.x, blocker.y - i) for i in range(1,3)}
                        coords_down = {(blocker.x, blocker.y + i) for i in range(3, 5)}

                    elif blocker.y == exit_row:
                        coords_up = {(blocker.x, blocker.y - i) for i in range(1,4)}
                        coords_down = {(blocker.x, blocker.y + 3)}

                if blocker.length == 2:
                    if blocker.y == exit_row - 1:
                        coords_up = {(blocker.x, blocker.y - 1)}
                        coords_down = {(blocker.x, blocker.y + i) for i in range(2,4)}

                    elif blocker.y == exit_row: 
                        coords_up = {(blocker.x, blocker.y - i) for i in range(1,3)}
                        coords_down = {(blocker.x, blocker.y + 2)}

                if (coords_up.intersection(self.occupied_coords)) or\
                (coords_down.intersection(self.occupied_coords)): 
                    return False
            return True
        # for 6x6 boards
        if self.dim_board == 6 and self.blockers[0].x == 5 and len(self.blockers) == 1:
            blocker = self.blockers[0]
            if blocker.y == 0:
                return not ({(5, 3), (5, 4), (5,5)}.intersection(self.occupied_coords))
            if blocker.y == 1:
                return not ({(5, 4), (5, 5)}.intersection(self.occupied_coords))
            if blocker.y == 2:
                return not ({(5,5)}.intersection(self.occupied_coords))
            
