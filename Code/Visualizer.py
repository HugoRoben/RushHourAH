import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

def random_color():
    return (random.random(), random.random(), random.random())

class Visualizer:
    @staticmethod
    
    def draw(grid):
        fig, ax = plt.subplots()
        # Draw grid lines
        for i in range(7):  # 7 lines to create 6x6 grid
            ax.axhline(i, color='black', linewidth=1)
            ax.axvline(i, color='black', linewidth=1)

        # Draw vehicles
        for y in range(6):
            for x in range(6):
                vehicle = grid.grid[y][x]
                if vehicle:
                    if vehicle._orientation == 'H':
                        color = random_color()
                        rect = patches.Rectangle((x, y), vehicle._length, 1, edgecolor='black', facecolor = color)
                        ax.add_patch(rect)
                    else:
                        color = random_color()
                        rect = patches.Rectangle((x, y), 1, vehicle._length, edgecolor='black', facecolor= color)
                        ax.add_patch(rect)

        for y in range(6):
            for x in range(6):
                vehicle = grid.grid[y][x]
                if vehicle:
                    # Display the order number
                    ax.text(x + 0.5, y + 0.5, str(vehicle._carid),
                            horizontalalignment='center',
                            verticalalignment='center',
                            fontsize=8, color='white')    

        plt.xlim(0, 6)
        plt.ylim(0, 6)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')  # Hide the default axes
        plt.show()