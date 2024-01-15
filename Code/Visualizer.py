# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import random
# from typing import Tuple

# def random_color():
#     """
#     Generate a random RGB color.

#     Returns:
#         Tuple[float, float, float]: A tuple representing an RGB color, with each component ranging from 0 to 1.
#     """
#     return (random.random(), random.random(), random.random())

# class Visualizer:
#     """
#     A class to visualize the Rush Hour game grid using matplotlib.

#     Attributes:
#         color_map (dict): A dictionary mapping car IDs to their respective colors.
#     """

#     color_map = {}

#     @staticmethod
#     def get_vehicle_color(car_id):
#         """
#         Get a consistent random color for a given vehicle. If the vehicle's color
#         does not exist in the color_map, it generates and assigns a new color.

#         Args:
#             car_id (str): The ID of the vehicle.

#         Returns:
#             Tuple[float, float, float]: The color (RGB tuple) associated with the vehicle.
#         """
#         if car_id not in Visualizer.color_map:
#             Visualizer.color_map[car_id] = random_color()
#         return Visualizer.color_map[car_id]

#     @staticmethod
#     def draw(grid):
#         """
#         Draw the current state of the Rush Hour game grid using matplotlib.

#         Args:
#             grid (Grid): The game grid to be visualized.

#         Preconditions:
#             The grid must be an instance of the Grid class with a valid grid attribute.

#         Postconditions:
#             Displays the current state of the grid with each vehicle represented in a distinct color.
#         """
#         fig, ax = plt.subplots()
#         grid_size = len(grid.grid)

#         # Draw grid lines
#         for i in range(grid_size + 1):
#             ax.axhline(i, color='black', linewidth=1)
#             ax.axvline(i, color='black', linewidth=1)

#         for vehicle in grid.vehicle_list:

#         # Draw vehicles
#         for y in range(grid_size):
#             for x in range(grid_size):
#                 vehicle = grid.grid[y][x]
#                 if vehicle is not None:
#                     color = Visualizer.get_vehicle_color(vehicle._carid)
#                     # Special color for the 'X' vehicle (usually red)
#                     if vehicle._carid == 'X': color = 'red'
#                     # Determine the orientation and draw the vehicle
#                     if vehicle._orientation == 'H':
#                         rect = patches.Rectangle((x, grid_size - y - 1), vehicle._length - 1, 1, edgecolor='black', facecolor=color)
#                     else:
#                         rect = patches.Rectangle((x, grid_size - y - vehicle._length), 1, vehicle._length, edgecolor='black', facecolor=color)
#                     ax.add_patch(rect)
#                     # Add vehicle ID text on the vehicle
#                     ax.text(x + 0.5, grid_size - y - 0.5, str(vehicle._carid),
#                             horizontalalignment='center', verticalalignment='center',
#                             fontsize=8, color='white', weight='bold')

#         plt.xlim(0, grid_size)
#         plt.ylim(0, grid_size)
#         plt.gca().set_aspect('equal', adjustable='box')
#         plt.axis('off')
#         plt.show()

# # Example usage
# # grid = Grid(6)
# # Visualizer.draw(grid)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from typing import Tuple

def random_color():
    """
    Generate a random RGB color.
    Returns:
        Tuple[float, float, float]: A tuple representing an RGB color, with each component ranging from 0 to 1.
    """
    return (random.random(), random.random(), random.random())

class Visualizer:
    """
    A class to visualize the Rush Hour game grid using matplotlib.
    Attributes:
        color_map (dict): A dictionary mapping car IDs to their respective colors.
    """

    color_map = {}

    @staticmethod
    def get_vehicle_color(car_id):
        """
        Get a consistent random color for a given vehicle. If the vehicle's color
        does not exist in the color_map, it generates and assigns a new color.
        Args:
            car_id (str): The ID of the vehicle.
        Returns:
            Tuple[float, float, float]: The color (RGB tuple) associated with the vehicle.
        """
        if car_id not in Visualizer.color_map:
            Visualizer.color_map[car_id] = random_color()
        return Visualizer.color_map[car_id]

    @staticmethod
    def draw(grid):
        """
        Draw the current state of the Rush Hour game grid using matplotlib.
        Args:
            grid (Grid): The game grid to be visualized.
            vehicles (list): List of vehicle objects to be drawn.
        Preconditions:
            The grid must be an instance of the Grid class with a valid grid attribute.
            Vehicles must be a list of vehicle objects with properties like position, orientation, and length.
        Postconditions:
            Displays the current state of the grid with each vehicle represented in a distinct color.
        """
        fig, ax = plt.subplots()
        grid_size = len(grid.grid)

        # Draw grid lines
        for i in range(grid_size + 1):
            ax.axhline(i, color='black', linewidth=1)
            ax.axvline(i, color='black', linewidth=1)

        # Draw vehicles
        for vehicle in grid.vehicle_list:
            x, y = vehicle._x, grid_size - vehicle._y - 1
            color = Visualizer.get_vehicle_color(vehicle._carid)
            if vehicle._carid == 'X': 
                color = 'red'
            if vehicle._orientation == 'H':
                rect = patches.Rectangle((x, y), vehicle._length, 1, edgecolor='black', facecolor=color)
                ax.add_patch(rect)
                for i in range(vehicle._length):
                    ax.text(x + i + 0.5, y + 0.5, str(vehicle._carid),
                            horizontalalignment='center', verticalalignment='center',
                            fontsize=8, color='white', weight='bold')
            else:
                rect = patches.Rectangle((x, y - vehicle._length + 1), 1, vehicle._length, edgecolor='black', facecolor=color)
                ax.add_patch(rect)
                for i in range(vehicle._length):
                    ax.text(x + 0.5, y - i + 0.5, str(vehicle._carid),
                            horizontalalignment='center', verticalalignment='center',
                            fontsize=8, color='white', weight='bold')

        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')
        plt.show()
