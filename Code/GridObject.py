# File for the class of the grid

import csv
from CarObject import vehicle

class Grid:
    # make a size by size grid
    def __init__(self, size):
        self.vehicle_list = []
        self.size = size
        self.grid = [[None for _ in range(size + 1)] for _ in range(size + 1)]

    def load_data(self, file):
        # Read CSV and create vehicles
        with open('gameboards/Rushhour6x6_1.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                CarId, orientation, col, row, length = row[0], row[1], int(row[2]) - 1, int(row[3]) - 1, int(row[4])
                self.add_vehicle(vehicle(CarId, orientation, col, row, length))
                self.vehicle_list.append(vehicle(CarId, orientation, col, row, length))
    
    # add a car object to the grid
    def add_vehicle(self, vehicle):
        x = vehicle._x
        y = vehicle._y

        if vehicle._orientation == 'H' and \
            all(self.grid[y][x + i] is None for i in range(vehicle._length)\
                if 0 <= x + i < self.size):
            
            for i in range(vehicle._length - 1):
                self.grid[y][x + i] = vehicle

        elif vehicle._orientation == 'V' and \
            all(self.grid[y + i][x] is None for i in range(vehicle._length)\
                if 0 <= y + i< self.size):
            
            for i in range(vehicle._length - 1):
                self.grid[y + i][x] = vehicle

    def is_path_clear(self, vehicle, steps):
        # Check if the path is clear for the given number of steps
        x = vehicle._x
        y = vehicle._y
        if vehicle._orientation == 'H':
            # for steps to the left
            if steps < 0: 
                # check if all tiles are empty after the move and inside the board
                return all(self.grid[y][x + i] == None\
                           for i in range(steps) if 0 <= x + i < self.size)

            # for steps to the right
            else: 
                # check if all tiles are empty after the move and inside the board
                return all(self.grid[y][x + vehicle._length + i] == None\
                           for i in range(steps) if 0 <= x + vehicle._length + i < self.size)

        else:
            # steps downward
            if steps < 0: 
                # check if all tiles are empty after the move and inside the board
                return all(self._grid[y + i][x] == None\
                           for i in range(steps) if 0 <= y + i < self.size)
            # steps upward
            else: 
                # check if all tiles are empty after the move and inside the board
                return all(self._grid[y + vehicle._length + i][x] == None\
                           for i in range(steps) if 0 <= y + vehicle._length + i < self.size)

    def move_vehicle(self, carid, steps):
        for vehicle in self.vehicle_list:
            if vehicle._carid == carid:
                this_vehicle = vehicle
        if self.is_path_clear(this_vehicle, steps):
            x = this_vehicle._x
            y = this_vehicle._y
            if this_vehicle._orientation == 'H':
                # clear the old poisitions of the vehicle
                self.grid[y][x:x + this_vehicle._length - 1] = [None] * this_vehicle._length
                this_vehicle._x = x + steps
                self.add_vehicle(this_vehicle)
            else:
                # clear the old poisitions of the vehicle
                for i in range(this_vehicle._length):
                    self.grid[y + i][x] = None
                this_vehicle._y = y + steps
                self.add_vehicle(this_vehicle)
            return True
        return False

    # def is_solved(self):
    #     # Check if the red car is at the exit
    #     for vehicle in self.grid[2]:
    #         if vehicle and vehicle.color == 'red':
    #             return vehicle.position[0] + vehicle.length == 6
    #     return False

