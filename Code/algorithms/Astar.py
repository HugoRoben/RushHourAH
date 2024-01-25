from ..classes.VehicleClass import Vehicle
from ..classes.RushClass import *
import heapq
from matplotlib import pyplot 


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

    def get_red_car(self, state):
        for vehicle in state.vehicles:
            if vehicle.id == 'X':
                red_car = vehicle
                return red_car
        # return None if red car not found
        return None
    
    def is_blocking(self, v, blocker):

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
        red_car = self.get_red_car(state)
        blocking_cars = []
        for v in self.vehicles:
            if v.x > red_car.x + 1 and v.orientation == 'V':
                if v.y == red_car.y - 1 or v.y == red_car.y or (v.y == red_car.y - 2 and v.length == 3):
                    blocking_cars.append(v)
        return blocking_cars

    def second_blockers(self, state):
        """get the cars blocking the cars that are blocking the red car"""
        blockers = self.get_blocking_cars(state)
        second_blockers = []
        for blocker in blockers:
            for v in state.vehicles:
                    if self.is_blocking(blocker, v):
                        second_blockers.append(v)
        return second_blockers
   
    def third_blockers(self, state, second_blockers, blockers):
        """get the car that are blocking the cars from second_blockers"""
        third_blockers = []
        for blocker in second_blockers:
            for v in state.vehicles:
                if v not in second_blockers and v not in blockers:
                        if self.is_blocking(blocker, v):
                            third_blockers.append(v)
        return third_blockers
    
    def fourth_blockers(self, state, third_blockers, second_blockers, blockers):
        """get the car that are blocking the cars from third_blockers"""
        fourth_blockers = []
        for blocker in third_blockers:
            for v in state.vehicles:
                if v not in third_blockers and v not in second_blockers and v not in blockers:
                        if self.is_blocking(blocker, v):
                            fourth_blockers.append(v)
        return fourth_blockers

    def three_long_blockers(self, state):
        blockers = self.get_blocking_cars(state)
        count = 0
        for v in blockers: 
            if v.length == 3: count +=1
        return count 

    def total_heuristic_function(self, state, prev_state):
        blockers = self.get_blocking_cars(state)
        second_blockers = self.second_blockers(state)
        third_blockers = self.third_blockers(state, second_blockers, blockers)
        fourth_blockers = self.fourth_blockers(state, third_blockers, second_blockers, blockers)

        blocking_cost = len(blockers) + len(second_blockers) + len(third_blockers) + len(fourth_blockers)
        extra_cost_long_cars = self.three_long_blockers(state)
        distance_cost = self.heuristic_distance_to_exit(state)

        distance_weight = 1
        if extra_cost_long_cars == 0:
            distance_weight = 2

        return blocking_cost + distance_cost * distance_weight + extra_cost_long_cars
        
    def heuristic_distance_to_exit(self, state):
        red_car = self.get_red_car(state)
        return (state.dim_board - 2 - red_car.x)

    def is_winning_state(self, state):
        """
        Check if the 'X' vehicle (red car) can exit the board.
        """
        return len(self.get_blocking_cars(state)) == 0
    
    def astar_search_single_ended(self, initial_state, max_iterations=100000000):
        # store the heuristic value of all the used states in a list to plot
        heuristic_list = []
        # calculate heuristic function of the starting state
        open_states = [HeapItem(self.total_heuristic_function(initial_state, initial_state), initial_state)]
        closed_states = set()
        open_set = {initial_state}
        iterations = 0

        while open_states:
            if iterations >= max_iterations:
                print("Maximum iterations reached, terminating search.")
                break

            current_state = heapq.heappop(open_states).rush_hour_obj

            if self.is_winning_state(current_state):
                pyplot.plot(heuristic_list)
                pyplot.show()
                return iterations

            # print(f"Current State: {current_state}")
            closed_states.add(current_state)

            for next_state in current_state.moves():
                if next_state not in closed_states and next_state not in open_set:
                    heapq.heappush(open_states, HeapItem(self.total_heuristic_function(next_state, current_state), next_state))
                    open_set.add(next_state)
                    heuristic_list.append(self.total_heuristic_function(next_state, current_state))
            # print(iterations)
            iterations += 1

        print("No solution found")
        pyplot.plot(heuristic_list)
        pyplot.show()
        return None
