'''
Class representing the visualisation of a solution for a rush hour game.
The class draws each state in a solution path and animates the states
after each other to see the path taken for the solution.
'''

import pygame
import random
from ..classes.RushClass import RushHour
from typing import Tuple, List

def random_color() -> Tuple[int, int, int]:
    """
    Generates a random colour for the vehicles.
    
    Returns:
        Tuple[int, int, int]: A tuple representing the RGB color values.
    """
    # lower max red value to keep clear distinction from the red car
    return (random.randint(0, 200), random.randint(0, 255),
            random.randint(0, 255))

class Visualizer:
    def __init__(self, width: int, height: int):
        """
        Initialize the Visualizer.

        Args:
            width (int): The width of the game window.
            height (int): The height of the game window.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.color_map = {}

    def get_vehicle_color(self, car_id: str):
        """
        Check if car already has a colour assigned, if not call random_color.

        Args:
        -----------------------------------------------------------------------
            car_id (str): The ID of the vehicle.

        Returns:
        -----------------------------------------------------------------------
            Tuple[int, int, int]: A tuple representing the RGB color values.
        """        
        if car_id not in self.color_map:
            self.color_map[car_id] = random_color()
        return self.color_map[car_id]

    def draw(self, rush_hour_state: RushHour):
        """
        Draws the board on screen given the configuration of the vehicles.

        Args:
        -----------------------------------------------------------------------
            rush_hour_state (RushHour): The state of the Rush Hour game to be
            visualized.
        """        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # fill the screen with white
        self.screen.fill((255, 255, 255))
        # initiate the grid
        grid_size = rush_hour_state.dim_board
        cell_size = self.screen.get_width() // grid_size
        # Draw the grid
        for x in range(grid_size):
            for y in range(grid_size):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size,\
                                   cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        # Draw vehicles
        for vehicle in rush_hour_state.vehicles:
            x, y = vehicle.x, vehicle.y
            if vehicle.orientation == 'H':
                rect = pygame.Rect(x * cell_size, y * cell_size,\
                                vehicle.length * cell_size, cell_size)
            else:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size,\
                                            vehicle.length * cell_size)

            color = self.get_vehicle_color(vehicle.id)
            # make the red car (car with id 'X) a red colour
            if vehicle.id == 'X':
                color = (255, 0, 0) 
            # draw the rects representing the vehicles on the board
            pygame.draw.rect(self.screen, color, rect)
        # update the screen
        pygame.display.flip()
        # run the game at 60fps
        self.clock.tick(60)

    def animate_solution(self, solution_path: List[RushHour], frame_delay=100):
        """
        Animate the sequence of states in the solution path.

        Args:
        -----------------------------------------------------------------------
            solution_path (list): A list of RushHour states representing the
            solution path.
            frame_delay (int): Delay between frames in milliseconds.
        """
        for state in solution_path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.draw(state)
            pygame.time.delay(frame_delay)