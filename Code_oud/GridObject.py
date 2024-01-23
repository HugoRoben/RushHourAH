# twee dingen bijhouden: 
# - totale delta per auto
# - alle stappen

import csv
from CarObject import vehicle

class Grid:
    def __init__(self, size):
        """
        Initialize a Grid object for the Rush Hour game.

        Args:
            size (int): The size of the grid (number of rows and columns).

        Preconditions:
            - size should be a positive integer.

        Postconditions:
            - A grid of the specified size is created with all cells initialized to None.
        """
        
        self.vehicle_dict = {}
        self.vehicle_list = []  # List of vehicles on the grid
        self.size = size
        # 2D grid initialization
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def load_data(self, filepath):
        """
        Load vehicle data from a CSV file and populate the grid with vehicles.

        Args:
            filepath (str): The path to the CSV file containing vehicle data.

        Preconditions:
            - The CSV file should exist and be in the correct format.

        Postconditions:
            - Vehicles from the CSV file are added to the grid if they fit.
        """
        with open(filepath, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                car_id, orientation, col, row, length = row
                vehicle_obj = vehicle(car_id, orientation, int(col) - 1, int(row) - 1, int(length))
                self.add_vehicle(vehicle_obj)


    def add_vehicle(self, vehicle):
        """
        Add a vehicle to the grid.

        Args:
            vehicle (Vehicle): The vehicle object to be added.

        Preconditions:
            - The vehicle should fit in the grid without overlapping with other vehicles.

        Postconditions:
            - The vehicle is added to the grid and vehicle list if there's sufficient space.
        """
        x, y = vehicle.x, vehicle.y
        if self.is_space_available(vehicle):
            for i in range(vehicle._length):
                if vehicle._orientation == 'H':
                    self.grid[y][x + i] = vehicle
                else:
                    self.grid[y + i][x] = vehicle
            # make a dictionary with key = carid, value = vehicle object
            self.vehicle_dict[vehicle._carid] = vehicle
            # self.vehicle_list.append(vehicle)

    def is_space_available(self, vehicle):
            """
            Check if there is enough space available on the grid to place the vehicle.

            Args:
                vehicle (Vehicle): The vehicle to check space for.

            Returns:
                bool: True if space is available, False otherwise.
            """
            x, y = vehicle.x, vehicle.y
            for i in range(vehicle._length):
                if vehicle._orientation == 'H':
                    if not (0 <= x + i < self.size and self.grid[y][x + i] is None):
                        return False
                else:
                    if not (0 <= y + i < self.size and self.grid[y + i][x] is None):
                        return False
            return True

    def is_path_clear(self, vehicle, steps):
        """
        Check if the path is clear for the vehicle to move the given number of steps.

        Args:
            vehicle (vehicle): The vehicle to check the path for.
            steps (int): The number of steps to move the vehicle.

        Returns:
            bool: True if the path is clear, False otherwise.

        Preconditions:
            - The vehicle should be within the bounds of the grid.
            - Steps should be an integer.
        """
        x, y = vehicle.x, vehicle.y
        length = vehicle._length

        if vehicle._orientation == 'H':
            start, end = (x + length, x + length + steps) if steps > 0 else (x + steps, x)
            return all(0 <= new_x < self.size and self.grid[y][new_x] is None for new_x in range(start, end))
        else:
            start, end = (y + length, y + length + steps) if steps > 0 else (y + steps, y)
            return all(0 <= new_y < self.size and self.grid[new_y][x] is None for new_y in range(start, end))

    def move_vehicle(self, carid, steps):
        """
        Move a vehicle on the grid if the path is clear.

        Args:
            carid (str): The ID of the vehicle to move.
            steps (int): The number of steps to move the vehicle.

        Returns:
            bool: True if the vehicle was moved, False otherwise.

        Preconditions:
            - The carid should correspond to a vehicle on the grid.
            - Steps should be an integer.
        """
        vehicle_to_move = self.vehicle_dict[carid]

        if vehicle_to_move._orientation == 'V': steps *= -1

        if vehicle_to_move and self.is_path_clear(vehicle_to_move, steps):
            self.clear_vehicle_position(vehicle_to_move)
            self.update_vehicle_position(vehicle_to_move, steps)

            # keep score for the total change in the position of the cars
            vehicle_to_move.TotalDelta += steps

        # else: print("move not possible")
    
    def clear_vehicle_position(self, vehicle):
        """
        Clear the current position of the vehicle on the grid.

        Args:
            vehicle (vehicle): The vehicle to clear the position of.
        """
        x, y = vehicle.x, vehicle.y
        for i in range(vehicle._length):
            if vehicle._orientation == 'H':
                self.grid[y][x + i] = None
            else:
                self.grid[y + i][x] = None

    def update_vehicle_position(self, vehicle, steps):
        """
        Update the position of the vehicle on the grid.

        Args:
            vehicle (vehicle): The vehicle to update the position of.
            steps (int): The number of steps to move the vehicle.

        Preconditions:
            - The new position should be within the grid boundaries.
        """
        if vehicle._orientation == 'H':
            vehicle.x += steps
        else:
            vehicle.y += steps
        self.add_vehicle(vehicle)

    def is_solved(self):
        """
        Check if the puzzle is solved, i.e., if the red car (car with id 'X') 
        has reached the exit.

        Returns:
            bool: True if the puzzle is solved, False otherwise.
        """
        # find the row the exit is at based on the size of the board
        # scan in the exit row for the red car (car with id 'X')
        for vehicle in self.vehicle_dict:
            if self.vehicle_dict[vehicle]._carid == 'X':
                # check if the end of the car is at the last column of the board
                return self.vehicle_dict[vehicle].x == self.size - 2