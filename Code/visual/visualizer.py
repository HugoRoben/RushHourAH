'''
Class representing the visualisation of a solution for a rush hour game.
The class draws each state in a solution path and animates the states
after each other to see the path taken for the solution.
'''

import pygame
import random
from ..classes.RushClass import RushHour

def random_color():
    """ Generates a random colour for the vehicles"""
    # lower max red value to keep clear distinction from the red car
    return (random.randint(0, 200), random.randint(0, 255), random.randint(0, 255))

class Visualizer:
    def __init__(self, width: int, height: int):
        # Initialise the game
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.color_map = {}

    def get_vehicle_color(self, car_id: str):
        """ Check if car already has a colour assigned, if not call random_color"""
        if car_id not in self.color_map:
            self.color_map[car_id] = random_color()
        return self.color_map[car_id]

    def draw(self, rush_hour_state: RushHour):
        """ Draws the board on screen given the configuration of the vehicles"""
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
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        # Draw vehicles
        for vehicle in rush_hour_state.vehicles:
            x, y = vehicle.x, vehicle.y
            if vehicle.orientation == 'H':
                rect = pygame.Rect(x * cell_size, y * cell_size, vehicle.length * cell_size, cell_size)
            else:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, vehicle.length * cell_size)

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

    def animate_solution(self, solution_path: list, frame_delay: int =100):
        """
        Animate the sequence of states as a solution path.
        """
        for state in solution_path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.draw(state)
            pygame.time.delay(frame_delay)