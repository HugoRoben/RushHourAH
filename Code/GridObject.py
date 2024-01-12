# File for the class of the grid

import csv
from CarObject import vehicle

class Grid:
    def __init__(self, size):
        self.vehicle_list = []
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def load_data(self, filepath):
        with open(filepath, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                car_id, orientation, col, row, length = row
                vehicle_obj = vehicle(car_id, orientation, int(col) - 1, int(row) - 1, int(length))
                self.add_vehicle(vehicle_obj)

    def add_vehicle(self, vehicle):
        x, y = vehicle._x, vehicle._y
        if self.is_space_available(vehicle):
            for i in range(vehicle._length):
                if vehicle._orientation == 'H':
                    self.grid[y][x + i] = vehicle
                else:
                    self.grid[y + i][x] = vehicle
            self.vehicle_list.append(vehicle)

    def is_space_available(self, vehicle):
        x, y = vehicle._x, vehicle._y
        for i in range(vehicle._length):
            if vehicle._orientation == 'H':
                if not (0 <= x + i < self.size and self.grid[y][x + i] is None):
                    return False
            else:
                if not (0 <= y + i < self.size and self.grid[y + i][x] is None):
                    return False
        return True

    def is_path_clear(self, vehicle, steps):
        x, y = vehicle._x, vehicle._y
        if vehicle._orientation == 'H':
            return self.check_horizontal_path(x, y, vehicle._length, steps)
        else:
            return self.check_vertical_path(x, y, vehicle._length, steps)

    def check_horizontal_path(self, x, y, length, steps):
        start, end = (x + length, x + length + steps) if steps > 0 else (x + steps, x)
        return all(0 <= new_x < self.size and self.grid[y][new_x] is None for new_x in range(start, end))

    def check_vertical_path(self, x, y, length, steps):
        start, end = (y + length, y + length + steps) if steps > 0 else (y + steps, y)
        return all(0 <= new_y < self.size and self.grid[new_y][x] is None for new_y in range(start, end))

    def move_vehicle(self, carid, steps):
        vehicle_to_move = next((v for v in self.vehicle_list if v._carid == carid), None)
        if vehicle_to_move and self.is_path_clear(vehicle_to_move, steps):
            self.clear_vehicle_position(vehicle_to_move)
            self.update_vehicle_position(vehicle_to_move, steps)
            return True
        return False

    def clear_vehicle_position(self, vehicle):
        x, y = vehicle._x, vehicle._y
        for i in range(vehicle._length):
            if vehicle._orientation == 'H':
                self.grid[y][x + i] = None
            else:
                self.grid[y + i][x] = None

    def update_vehicle_position(self, vehicle, steps):
        if vehicle._orientation == 'H':
            vehicle._x += steps
        else:
            vehicle._y += steps
        self.add_vehicle(vehicle)

    def is_solved(self):
        # Check if the red car is at the exit
        # find the row the exit is at based on the size of the board
        if self.size // 2 == 0: exit_row = self.size / 2
        else: exit_row = self.size // 2
        # scan in the exit row for the red car (car with id 'X')
        for vehicle in self.grid[exit_row]:
            if vehicle and vehicle._carid == 'X':
                # check if the end of the car is at the last column of the board
                return vehicle._x + vehicle._length == self.size
        return False

