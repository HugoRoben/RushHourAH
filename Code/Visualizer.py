import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from typing import Tuple
from matplotlib.animation import FuncAnimation

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
    def setup_interactive_mode():
        plt.ion()  # Turn on interactive mode

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
        plt.close()  # Clear the current figure
        fig, ax = plt.subplots()
        grid_size = len(grid.grid)

        # Draw grid lines
        for i in range(grid_size + 1):
            ax.axhline(i, color='black', linewidth=1)
            ax.axvline(i, color='black', linewidth=1)

        # Draw vehicles
        for vehicle in grid.vehicle_dict:

            vehicle_obj = grid.vehicle_dict[vehicle]
            x, y = vehicle_obj.x, grid_size - vehicle_obj.y - 1
            
            color = Visualizer.get_vehicle_color(vehicle_obj._carid)
            if vehicle_obj._carid == 'X': 
                color = 'red'
            if vehicle_obj._orientation == 'H':
                rect = patches.Rectangle((x, y), vehicle_obj._length, 1, edgecolor='black', facecolor=color)
                ax.add_patch(rect)
                for i in range(vehicle_obj._length):
                    ax.text(x + i + 0.5, y + 0.5, str(vehicle_obj._carid),
                            horizontalalignment='center', verticalalignment='center',
                            fontsize=8, color='white', weight='bold')
            else:
                rect = patches.Rectangle((x, y - vehicle_obj._length + 1), 1, vehicle_obj._length, edgecolor='black', facecolor=color)
                ax.add_patch(rect)
                for i in range(vehicle_obj._length):
                    ax.text(x + 0.5, y - i + 0.5, str(vehicle_obj._carid),
                            horizontalalignment='center', verticalalignment='center',
                            fontsize=8, color='white', weight='bold')

        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')
        plt.draw()  # Redraw the current figure
        plt.pause(0.1)  # Pause for a short period to update the plot
