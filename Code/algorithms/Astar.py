'''
Class that performs a (weighted) A* search algorithm based on the 
cost of cars blocking the red car, the length of the cars
blocking the red car and the distance of the red car to the exit.
'''

from ..classes.RushClass import *
import heapq

class HeapItem:
    '''
    Class created to ensure the list with states can be sorted,
    by assigning a priority number to each state.
    In case the heuristic cost of states is equal, less than
    is defined as the lowest priority number
    '''
    def __init__(self, priority, rush_hour_obj):
        self.priority = priority
        self.rush_hour_obj = rush_hour_obj

    def __lt__(self, other):
        return self.priority < other.priority

class Astar:
    '''
    Class performing the A* algorithm
    '''
    def __init__(self, begin_state) -> None:
        self.begin_state = begin_state
        self.vehicles = begin_state.vehicles
        self.left = False

    def is_red_car_left(self, state):
        '''
        Check if the red car has been in the left-halve of the board.
        '''
        red_car = self.get_red_car(state)
        if red_car.x <= 3: self.left = True
        

    def get_red_car(self, state):
        '''
        Get the red car from the dictionary of vehicles in a state
        '''
        for vehicle in state.vehicles:
            if vehicle.id == 'X':
                red_car = vehicle
                return red_car
        # return None if red car not found
        return None
    
    def is_blocking(self, v, blocker):
        '''
        Check if 'blocker' is blocking 'v'
        '''
        # if horziontal cars not on the same row, no blocking is possible
        if v.orientation == 'H' and blocker.orientation == 'H' and v.y != blocker.y:
            return False
        # if vertical cars not on the same row, no blocking is possible
        if v.orientation == 'V' and blocker.orientation == 'V' and v.x != blocker.x:
            return False

        # Horizontal vehicle blocking
        if blocker.orientation == 'H':
            return self.is_horizontally_blocking(blocker, v)

        # Vertical vehicle blocking
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
        '''
        Get the cars blocking the 'X' car (red car)
        '''
        # get teh red car
        red_car = self.get_red_car(state)
        blocking_cars = []
        # iterate through vehicle set and add blocking vehicles to the list
        for v in state.vehicles:
            # horizontal cars can not block the red car
            if v.x > red_car.x + 1 and v.orientation == 'V':
                if v.y == red_car.y - 1 or v.y == red_car.y or (v.y == red_car.y - 2 and v.length == 3):
                    blocking_cars.append(v)
        return blocking_cars
    
    def blocking_cars_iterative(self, state, max_depth):
        '''
        Iteratively find all cars blocking other cars, starting with cars
        blocking the 'X' car up to the max_depth
        '''
        # keep track of the vheicles already considered as blockers
        already_considered = set()
        # start with the cars directly blocking the red car as current blockers
        current_level_blockers = set(self.get_blocking_cars(state))

        all_blockers = set(current_level_blockers)
        already_considered.update(current_level_blockers)

        for depth in range(2, max_depth + 1):
            next_level_blockers = set()
            # iterate through current blockers to find what cars block current blockers
            for blocker in current_level_blockers:
                for v in state.vehicles:
                    if self.is_blocking(blocker, v) and v not in already_considered:
                        next_level_blockers.add(v)
                        already_considered.add(v)

            current_level_blockers = next_level_blockers
            # add current blockers to all blockers
            all_blockers.update(current_level_blockers)
        return all_blockers

    def three_long_blockers(self, state):
        '''
        Calculate how many of the cars blocking the red car directly
        have a length of three
        '''
        blockers = self.get_blocking_cars(state)
        count = 0
        for v in blockers: 
            if v.length == 3: count +=1
        return count 

    def heuristic_distance_to_exit(self, state):
        '''
        Calculate distance to exit for 'X' car (red car)
        '''
        red_car = self.get_red_car(state)
        return (state.dim_board - 2 - red_car.x)
    
    def total_heuristic_function(self, state):
        '''
        Calculate the sum of all the cost functions for a state.
        '''
        # check if red car has been in left halve of the board
        self.is_red_car_left(state)
        # initial weights for the costs
        length_weight = 1
        distance_weight = 1
        # calculate the different costs
        blocking_cost = len(self.blocking_cars_iterative(state, 3))
        extra_cost_long_cars = self.three_long_blockers(state)
        distance_cost = self.heuristic_distance_to_exit(state)
        # if blocking cars with length three, change weights
        if extra_cost_long_cars >= 1:
            distance_weight = 0
            length_weight = 2 
        # if not self.left: distance_weight = 0
        # if extra_cost_long_cars >= 1 and self.left:
        #     distance_weight = 0
        # if no more blocking cars with length three, increase weight for Manhattan distance
        if extra_cost_long_cars == 0:
            distance_weight = 2

        return blocking_cost + distance_cost * distance_weight + extra_cost_long_cars * length_weight

    def is_winning_state(self, state):
        """
        Check if the 'X' vehicle (red car) can exit the board.
        """
        # if no more blocking cars, game is won
        return len(self.get_blocking_cars(state)) == 0
    
    def reconstruct_path(self, end_state):
        """
        Reconstruct the solution path from the end state.
        """
        path = []
        # start with the end state (solution)
        current_state = end_state
        # every state has a parent, except for the intital state
        # keep backtracking untill initial state is found
        while current_state is not None:
            # insert the state in the solution path
            path.insert(0, current_state)
            # update current state to its' parent state
            current_state = current_state.parent
        return path
    
    def is_solvable(self, state):
        '''
        checks if there is only one blocking car left which can be moved to solve the board
        '''
        last_column = [row[-1] for row in state.get_board()]
        blocking_cars = self.get_blocking_cars(state)
        # check if only one car is blocking the red car
        if len(blocking_cars) == 1:
            # for 9x9 boards
            if state.dim_board == 9 and blocking_cars[0].x == 8:
                blocker = blocking_cars[0]
                if blocker.length == 3:
                    # check if the blocking car is in a position it can move out of the free the exit
                    # without having to move other vehicles
                    return (all(cell == ' ' or (cell == blocker.id) for cell in last_column[0:6])) or\
                            (all(cell == ' ' or (cell == blocker.id) for cell in last_column[2:8])) or \
                            (all(cell == ' ' or (cell == blocker.id) for cell in last_column[1:6])) or \
                            (all(cell == ' ' or (cell == blocker.id) for cell in last_column[3:8])) or \
                            (all(cell == ' ' or (cell == blocker.id) for cell in last_column[1:7])) or \
                            (all(cell == ' ' or (cell == blocker.id) for cell in last_column[4:8]))

            # for 6x6 boards
            if state.dim_board == 6 and blocking_cars[0].x == 5:
                blocker = blocking_cars[0]
                if blocker.length == 3:
                    # check if the blocking car is in a position it can move out of the free the exit
                    # without having to move other vehicles
                    return all(
                        cell == ' ' or (cell == blocker.id) 
                        for cell in last_column[blocker.y:state.dim_board]
                    )
            
    def astar_search_single_ended(self, initial_state, max_iterations=100000000):
        '''
        Performs A* search algorithm
        '''
        solution_path = []
        # calculate heuristic function of the starting state
        open_states = [HeapItem(self.total_heuristic_function(initial_state), initial_state)]
        # keep track of visited states in a set
        closed_states = set()
        # keep the states to be visited in a set
        open_set = {initial_state}
        iterations = 0

        while open_states:
            if iterations >= max_iterations:
                print("Maximum iterations reached")
                break
            # pop the state with the lowest cost from the list
            current_state = heapq.heappop(open_states).rush_hour_obj

            # check if the game is won or the game is in a state where it is directly solvable
            if self.is_winning_state(current_state) or self.is_solvable(current_state):
                # reconstruct the path taken for the solution
                solution_path = self.reconstruct_path(current_state)
                # return the path
                return {'solution': solution_path}
            
            # if no solution, add the current state to the closed states
            closed_states.add(current_state)

            # generate the states to be visited, with option to generate look-ahead
            # states specified by depth
            future_states = self.begin_state.generate_future_states(current_state, depth=1)

            for state in future_states:
                # if a state is a winning state, break and return path
                if self.is_winning_state(state) or self.is_solvable(state):
                    solution_path = self.reconstruct_path(state)
                    return {'solution': solution_path}
                
                # check if state is not already visited or in the set with open states
                if state not in closed_states and state not in open_set:
                    # calculate cost of the state and add to the list
                    heapq.heappush(open_states, HeapItem(self.total_heuristic_function(state), state))
                    open_set.add(state)
                    
            iterations += 1
        # if no more states to be visited, return None
        print("No solution found")
        return None