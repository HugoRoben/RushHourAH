import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

def random_color():
    return (random.random(), random.random(), random.random())

class Visualizer:
    color_map = {}

    @staticmethod
    def get_vehicle_color(car_id):
        if car_id not in Visualizer.color_map:
            Visualizer.color_map[car_id] = random_color()
        return Visualizer.color_map[car_id]

    @staticmethod
    def draw(grid):
        fig, ax = plt.subplots()
        grid_size = len(grid.grid)

        # Draw grid lines
        for i in range(grid_size + 1):
            ax.axhline(i, color='black', linewidth=1)
            ax.axvline(i, color='black', linewidth=1)

        # Draw vehicles
        for y in range(grid_size - 1, -1, -1):
            for x in range(grid_size):
                vehicle = grid.grid[grid_size - 1 - y][x]
                if vehicle:
                    color = Visualizer.get_vehicle_color(vehicle._carid)
                    if vehicle._carid == 'X': color = 'red'
                    if vehicle._orientation == 'H':
                        rect = patches.Rectangle((x, y), vehicle._length - 1, 1, edgecolor='black', facecolor=color)
                    else:
                        rect = patches.Rectangle((x, y), 1, vehicle._length - 1, edgecolor='black', facecolor=color)
                    ax.add_patch(rect)
                    ax.text(x + 0.5, y + 0.5, str(vehicle._carid),
                            horizontalalignment='center', verticalalignment='center',
                            fontsize=8, color='white', weight='bold')

        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')
        plt.show()

# Example usage
# grid = Grid(6)
# Visualizer.draw(grid)
