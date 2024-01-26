from ..classes.VehicleClass import Vehicle
from ..classes.RushClass import *
import heapq
from ..visual.visualizer import *


class HeapItem:
    def __init__(self, priority, rush_hour_obj):
        self.priority = priority
        self.rush_hour_obj = rush_hour_obj

    def __lt__(self, other):
        return self.priority < other.priority

class Astar:
    def __init__(self, begin_state) -> None:
        self.begin_state = begin_state
        self.vehicles = begin_state.vehicles
        self.left = False

    def is_red_car_left(self, state):
        '''Check if the red car has been in the left-halve of the board.'''
        red_car = self.get_red_car(state)
        if red_car.x <= 3: self.left = True
        

    def get_red_car(self, state):
        '''Get the red car from the dictionary of vehicles in a state'''
        for vehicle in state.vehicles:
            if vehicle.id == 'X':
                red_car = vehicle
                return red_car
        # return None if red car not found
        return None
    
    def is_blocking(self, v, blocker):
        '''Check if 'blocker' is blocking 'v' '''

        if v.orientation == 'H' and blocker.orientation == 'H' and v.y != blocker.y:
            return False
        if v.orientation == 'V' and blocker.orientation == 'V' and v.x != blocker.x:
            return False

        # Horizontal vehicle blocking scenarios
        if blocker.orientation == 'H':
            return self.is_horizontally_blocking(blocker, v)

        # Vertical vehicle blocking scenarios
        if blocker.orientation == 'V':
            return self.is_vertically_blocking(blocker, v)

    def is_horizontally_blocking(self, blocker, target):
        """
        Check if a horizontally oriented 'vehicle' is blocking 'target'.
        """
        blocker_end = blocker.x + blocker.length
        if target.orientation == 'H':
            return blocker_end == target.x or target.x + target.length == blocker.x
        if target.orientation == 'V':
            if blocker.y == target.y + target.length or blocker.y == target.y - 1:
                return any(target.x == pos for pos in range(blocker.x, blocker_end))

    def is_vertically_blocking(self, blocker, target):
        """
        Check if a vertically oriented 'vehicle' is blocking 'target'.
        """
        blocker_end = blocker.y + blocker.length
        if target.orientation == 'V':
            return blocker.y == target.y + target.length or blocker_end == target.y 
        if target.orientation == 'H':
            return blocker.x == target.x + target.length or blocker.x == target.x - 1

    def get_blocking_cars(self, state):
        '''Get the cars blocking the 'X' car (red car)'''
        red_car = self.get_red_car(state)
        blocking_cars = []
        for v in self.vehicles:
            if v.x > red_car.x + 1 and v.orientation == 'V':
                if v.y == red_car.y - 1 or v.y == red_car.y or (v.y == red_car.y - 2 and v.length == 3):
                    blocking_cars.append(v)
        return blocking_cars
    
    def blocking_cars_iterative(self, state, max_depth):
        '''Iteratively find all cars blocking other cars, starting with cars
        blocking the 'X' car up to the max_depth'''
        already_considered = set()
        current_level_blockers = set(self.get_blocking_cars(state))
        all_blockers = set(current_level_blockers)
        already_considered.update(current_level_blockers)

        for depth in range(2, max_depth + 1):
            next_level_blockers = set()
            for blocker in current_level_blockers:
                for v in state.vehicles:
                    if self.is_blocking(blocker, v) and v not in already_considered:
                        next_level_blockers.add(v)
                        already_considered.add(v)

            current_level_blockers = next_level_blockers
            all_blockers.update(current_level_blockers)

        return all_blockers

    def three_long_blockers(self, state):
        '''Calculate how many of the blocking cars have a length of three'''
        blockers = self.get_blocking_cars(state)
        count = 0
        for v in blockers: 
            if v.length == 3: count +=1
        return count 

    def heuristic_distance_to_exit(self, state):
        '''Calculate distance to exit for 'X' car (red car)'''
        red_car = self.get_red_car(state)
        return (state.dim_board - 2 - red_car.x)
    
    def total_heuristic_function(self, state):
        '''Calculate the sum of all the cost functions for a state.'''

        self.is_red_car_left(state)

        length_weight = 1
        distance_weight = 1

        blocking_cost = len(self.blocking_cars_iterative(state, 3))
        extra_cost_long_cars = self.three_long_blockers(state)
        distance_cost = self.heuristic_distance_to_exit(state)

        if extra_cost_long_cars >= 1:
            # distance_weight = 0
            length_weight = 2 
        if not self.left: distance_weight = -2
        if extra_cost_long_cars >= 1 and self.left:
            distance_weight = 0
        if extra_cost_long_cars == 0:
            distance_weight = 2

        return blocking_cost + distance_cost * distance_weight + extra_cost_long_cars * length_weight

    def is_winning_state(self, state):
        """
        Check if the 'X' vehicle (red car) can exit the board.
        """
        return len(self.get_blocking_cars(state)) == 0
    
    def reconstruct_path(self, end_state):
        """
        Reconstruct the solution path from the end state.
        """
        path = []
        current_state = end_state
        while current_state is not None:
            path.insert(0, current_state)
            current_state = current_state.parent
        return path

    def astar_search_single_ended(self, initial_state, max_iterations=100000000):
        '''Performs the actual algorithm'''
        solution_path = []
        # calculate heuristic function of the starting state
        open_states = [HeapItem(self.total_heuristic_function(initial_state), initial_state)]
        closed_states = set()
        open_set = {initial_state}
        iterations = 0

        while open_states:
            if iterations >= max_iterations:
                print("Maximum iterations reached")
                break

            current_state = heapq.heappop(open_states).rush_hour_obj
            if (iterations % 1000 == 0):
                visualizer = Visualizer(600, 600)
                visualizer.draw(current_state)

            if self.is_winning_state(current_state):
                solution_path = self.reconstruct_path(current_state)
                visualizer = Visualizer(600, 600) 
                visualizer.animate_solution(solution_path)
                return solution_path

            closed_states.add(current_state)
            future_states = self.begin_state.generate_future_states(current_state, depth=1)
            for state in future_states:
                if state not in closed_states and state not in open_set:
                    heapq.heappush(open_states, HeapItem(self.total_heuristic_function(state), state))
                    open_set.add(state)

            # for move in current_state.moves():
            #     if move not in closed_states and move not in open_set: 
            #         heapq.heappush(open_states, HeapItem(self.total_heuristic_function(move), move))
            #         open_set.add(move)

            iterations += 1
        print("No solution found")
        return None