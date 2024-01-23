from Code.algorithms.Astar import Astar
from ..classes.VehicleClass import Vehicle
from ..classes.RushClass import *
from matplotlib import pyplot

class IDAstar(Astar):
    def __init__(self, begin_state):
        super().__init__(begin_state)

    def idastar_search(self, initial_state, max_iterations=100):
        threshold = self.total_heuristic_function(initial_state, initial_state)
        iterations = 0

        while True:
            if iterations >= max_iterations:
                print("Maximum iterations reached, terminating search.")
                return None

            min_exceeded_threshold, solution = self.search(initial_state, 0, threshold)
            if solution is not None:
                return solution

            if min_exceeded_threshold is None:
                print("No solution found")
                return None

            threshold = min_exceeded_threshold
            iterations += 1

    def search(self, state, g, threshold):
        f = g + self.total_heuristic_function(state, state)
        if f > threshold:
            return f, None

        if self.is_winning_state(state):
            return None, state

        min_exceeded_threshold = None
        for next_state in state.moves():
            temp_threshold, solution = self.search(next_state, state.move_count, threshold)
            if solution is not None:
                return None, solution
            if temp_threshold is not None:
                if min_exceeded_threshold is None:
                    min_exceeded_threshold = temp_threshold
                else:
                    min_exceeded_threshold = min(min_exceeded_threshold, temp_threshold)

        return min_exceeded_threshold, None



# class IDAStar:
#     def __init__(self, begin_state):
#         self.begin_state = begin_state

#     def ida_star_search(self):
#         threshold = self.heuristic(self.begin_state)
#         while True:
#             visited = set()
#             temp, new_threshold = self.search(self.begin_state, 0, threshold, visited)
#             if temp is not None:
#                 return temp
#             if new_threshold == float('inf'):
#                 return None
#             threshold = new_threshold

#     def search(self, state, g, threshold, visited):
#         f = g + self.heuristic(state)
#         if f > threshold or state in visited:
#             return None, f
#         visited.add(state)
#         if state.is_solved():
#             return g, f  # Return the depth at which the solution was found
#         min_threshold = float('inf')
#         for next_state in state.moves():
#             temp, new_threshold = self.search(next_state, g + 1, threshold, visited)
#             if temp is not None:
#                 return temp, new_threshold
#             if new_threshold < min_threshold:
#                 min_threshold = new_threshold
#         return None, min_threshold

#     def heuristic(self, state):
#         red_car = self.get_red_car(state)
#         if not red_car:
#             return float('inf')  # No solution possible if the red car is not found

#         distance_to_exit = state.dim_board - (red_car.x + red_car.length)
#         blocking_vehicles = 0
#         for vehicle in state.vehicles:
#             if vehicle.orientation == 'V' and vehicle.x > red_car.x:
#                 if red_car.y >= vehicle.y and red_car.y < vehicle.y + vehicle.length:
#                     blocking_vehicles += 1

#         return distance_to_exit + blocking_vehicles

#     def get_red_car(self, state):
#         for vehicle in state.vehicles:
#             if vehicle.id == 'X':
#                 return vehicle
#         return None

#     def is_solved(self, state):
#         red_car = self.get_red_car(state)
#         if red_car and red_car.x + red_car.length == state.dim_board:
#             return True
#         return False
