# import pygame
# import random

# def random_color():
#     """
#     Generate a random RGB color.
#     Returns:
#         Tuple[int, int, int]: A tuple representing an RGB color, with each component ranging from 0 to 255.
#     """
#     return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# class Visualizer:
#     def __init__(self, width, height):
#         self.screen = pygame.display.set_mode((width, height))
#         self.clock = pygame.time.Clock()
#         self.color_map = {}

#     def get_vehicle_color(self, car_id):
#         """
#         Get a consistent random color for a given vehicle. If the vehicle's color
#         does not exist in the color_map, it generates and assigns a new color.
#         Args:
#             car_id (str): The ID of the vehicle.
#         Returns:
#             Tuple[int, int, int]: The color (RGB tuple) associated with the vehicle.
#         """
#         if car_id not in self.color_map:
#             self.color_map[car_id] = random_color()
#         return self.color_map[car_id]

#     def draw(self, grid):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()

#         self.screen.fill((255, 255, 255))  # Fill the screen with a white color

#         grid_size = len(grid.grid)
#         cell_size = self.screen.get_width() // grid_size

#         # Draw grid
#         for x in range(grid_size):
#             for y in range(grid_size):
#                 rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
#                 pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Draw grid lines

#         # Draw vehicles
#         for vehicle in grid.vehicle_dict.values():
#             vehicle_obj = vehicle
#             x, y = vehicle_obj.x, vehicle_obj.y
#             if vehicle_obj._orientation == 'H':
#                 rect = pygame.Rect(x * cell_size, y * cell_size, vehicle_obj._length * cell_size, cell_size)
#             else:
#                 rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, vehicle_obj._length * cell_size)

#             color = self.get_vehicle_color(vehicle_obj._carid)
#             if vehicle_obj._carid == 'X':
#                 color = (255, 0, 0)  # Set color to red for the vehicle with ID 'X'

#             pygame.draw.rect(self.screen, color, rect)  # Draw vehicle as a rectangle

#         pygame.display.flip()
#         self.clock.tick(60)

import pygame
import random

def random_color():
    """ Generates a random colour for the vehicles"""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Visualizer:
    def __init__(self, width, height):
        # Initialise the game
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.color_map = {}

    def get_vehicle_color(self, car_id):
        """ Check if car already has a colour assigned, if not call random_color"""
        if car_id not in self.color_map:
            self.color_map[car_id] = random_color()
        return self.color_map[car_id]

    def draw(self, rush_hour_state):
        """ Draws the board on screen given the configuration of the vehicles"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.screen.fill((255, 255, 255))  # Fill the screen with white

        grid_size = rush_hour_state.dim_board
        cell_size = self.screen.get_width() // grid_size

        # Draw grid
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
            if vehicle.id == 'X':
                color = (255, 0, 0)  # Red for the target vehicle

            pygame.draw.rect(self.screen, color, rect)

        pygame.display.flip()
        self.clock.tick(60)


    def animate_solution(self, solution_path, frame_delay=100):
        """
        Animate the sequence of states as a solution path.

        Args:
        solution_path (list): A list of RushHour states representing the solution path.
        frame_delay (int): Time delay between frames in milliseconds.
        """
        for state in solution_path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.draw(state)
            pygame.time.delay(frame_delay)
