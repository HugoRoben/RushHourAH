from ..classes.RushClass import RushHour
from ..classes.VehicleClass import Vehicle
import heapq
from typing import Optional, List, Set, Dict, Union

class HeapItem:
    """
    Represents an item in the heap used in the A* search algorithm, with a
    priority for sorting.

    Attributes:
    ---------------------------------------------------------------------------
        priority (int): The priority of this item in the heap.
        rush_hour_obj (RushHour): The Rush-Hour game state associated with this
        heap item.
    """
    def __init__(self, priority: int, rush_hour_obj: RushHour):
        self.priority = priority
        self.rush_hour_obj = rush_hour_obj

    def __lt__(self, other: 'HeapItem'):
        return self.priority < other.priority

class Astar:
    """
    Implements a weighted A* search algorithm for solving the Rush Hour puzzle, 
    using heuristics based on the cost of cars blocking the red car, the length
    of these cars, and the distance of the red car to the exit.

    Attributes:
    ---------------------------------------------------------------------------
        begin_state (RushHour): The initial state of the Rush Hour game.
        vehicles (Set[Vehicle]): A set of vehicles in the game.
    """

    def __init__(self, begin_state: RushHour) -> None:
        """
        Initializes the Astar instance with the initial Rush Hour state.

        Args:
        -----------------------------------------------------------------------
            begin_state (RushHour): The initial state of the Rush Hour game.
        """
        self.begin_state = begin_state
        self.vehicles = begin_state.vehicles

    def is_blocking(self, v: Vehicle, blocker: Vehicle) -> bool:
        """
        Check if 'blocker' is blocking 'v'.

        Args:
        -----------------------------------------------------------------------
            v (Vehicle): The target Vehicle.
            blocker (Vehicle): The potentially blocking Vehicle.

        Returns:
        -----------------------------------------------------------------------
            bool: True if 'blocker' is blocking 'v', False otherwise.
        """
        # if horziontal cars not on the same row, no blocking is possible
        if v.orientation == 'H' and blocker.orientation == 'H'\
            and v.y != blocker.y:
            return False
        # if vertical cars not on the same row, no blocking is possible
        if v.orientation == 'V' and blocker.orientation == 'V'\
            and v.x != blocker.x:
            return False

        # Horizontal vehicle blocking
        if blocker.orientation == 'H':
            return self.is_horizontally_blocking(blocker, v)

        # Vertical vehicle blocking
        if blocker.orientation == 'V':
            return self.is_vertically_blocking(blocker, v)

    def is_horizontally_blocking(self, blocker: Vehicle, target: Vehicle)\
                                                                    -> bool:
        """
        Check if a horizontally oriented 'vehicle' is blocking 'target'.

        Args:
        -----------------------------------------------------------------------
            blocker (Vehicle): The potentially blocking horizontally oriented
            Vehicle.
            target (Vehicle): The target Vehicle.

        Returns:
        -----------------------------------------------------------------------
            bool: True if 'blocker' is blocking 'target', False otherwise.
        """
        blocker_end = blocker.x + blocker.length
        if target.orientation == 'H':
            return blocker_end == target.x or\
                target.x + target.length == blocker.x
        if target.orientation == 'V':
            if blocker.y == target.y + target.length or\
                blocker.y == target.y - 1:
                return any(target.x == x for x in range(blocker.x,blocker_end))

    def is_vertically_blocking(self, blocker: Vehicle, target: Vehicle) -> bool:
        """
        Check if a vertically oriented 'vehicle' is blocking 'target'.

        Args:
        -----------------------------------------------------------------------
            blocker (Vehicle): The potentially blocking vertically oriented
            Vehicle.
            target (Vehicle): The target Vehicle.

        Returns:
        -----------------------------------------------------------------------
            bool: True if 'blocker' is blocking 'target', False otherwise.
        """
        blocker_end = blocker.y + blocker.length
        if target.orientation == 'V':
            return blocker.y == target.y + target.length or\
                blocker_end == target.y 
        if target.orientation == 'H':
            return blocker.x == target.x + target.length or\
                blocker.x == target.x - 1
        
    def blocking_cars_iterative(self, state: RushHour, max_depth: int)\
                                                        -> Set[Vehicle]:
        """
        Iteratively finds all cars blocking other cars, starting with cars
        blocking the 'X' car up to the max_depth.

        Args:
        -----------------------------------------------------------------------
            state (RushHour): The Rush Hour game state.
            max_depth (int): The maximum depth to search for blocking cars.

        Returns:
        -----------------------------------------------------------------------
            Set[Vehicle]: A set of all vehicles blocking other vehicles.
        """
        # keep track of the vehicles already considered as blockers
        already_considered = set()
        # start with the cars directly blocking the red car as current blockers
        current_level_blockers = set(state.blockers)

        all_blockers = set(current_level_blockers)
        already_considered.update(current_level_blockers)

        for depth in range(2, max_depth + 1):
            next_level_blockers = set()
            # iterate through current blockers to find what cars block the cars
            # in current_blockers
            for blocker in current_level_blockers:
                for v in state.vehicles:
                    if self.is_blocking(blocker, v) and\
                                v not in already_considered:
                        # add new found blocking car
                        next_level_blockers.add(v)
                        already_considered.add(v)

            current_level_blockers = next_level_blockers
            # add current blockers to all blockers
            all_blockers.update(current_level_blockers)
        return all_blockers
    
    def three_long_blockers(self, state: RushHour) -> int:
        """
        Calculate how many of the cars blocking the red car directly
        have a length of three.

        Args:
        -----------------------------------------------------------------------
            state (RushHour): The Rush Hour game state.

        Returns:
        -----------------------------------------------------------------------
            int: The count of blocking cars with a length of three.
        """
        blockers = state.blockers
        count = 0
        for v in blockers: 
            if v.length == 3: count +=1
        return count 

    def Manhattan_distance_to_exit(self, state: RushHour) -> int:
        """
        Calculate the Manhattan distance to the exit for 'X' car (red car).

        Args:
        -----------------------------------------------------------------------
            state (RushHour): The Rush Hour game state.

        Returns:
        -----------------------------------------------------------------------
            int: The Manhattan distance to the exit.
        """
        return (state.dim_board - 2 - state.red_car.x)
    
    def total_cost_function(self, state: RushHour) -> int:
        """
        Calculate the sum of all the cost functions for a state.

        Args:
        -----------------------------------------------------------------------
            state (RushHour): The Rush Hour game state.

        Returns:
        -----------------------------------------------------------------------
            int: The total heuristic cost for the state.
        """
        # initial weights for the costs
        length_weight = 1
        distance_weight = 1
        blocker_weight = 1

        # calculate the different costs
        blocking_cost = len(self.blocking_cars_iterative(state, 3))
        extra_cost_long_cars = self.three_long_blockers(state)
        distance_cost = self.Manhattan_distance_to_exit(state)

        # determine te weights based on the current state
        if extra_cost_long_cars >= 1:
            distance_weight = -2
            length_weight = 2
        if extra_cost_long_cars == 0:
            distance_weight = 2

        return blocking_cost * blocker_weight + distance_cost * distance_weight +\
                    extra_cost_long_cars * length_weight
    
    def reconstruct_path(self, end_state: RushHour) -> List[RushHour]:
        """
        Reconstruct the solution path from the end state.

        Args:
        -----------------------------------------------------------------------
            end_state (RushHour): The end state of the solution.

        Returns:
        -----------------------------------------------------------------------
            List[RushHour]: A list of states representing the solution path.
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
            
    def astar_search(self, initial_state: RushHour, max_iterations: int=100000000)\
                -> Optional[Dict[str, Union[int, List[RushHour]]]]:
        """
        Performs A* search algorithm to solve the Rush Hour game.

        Args:
        -----------------------------------------------------------------------
            initial_state (RushHour): The initial state of the game.
            max_iterations (int): The maximum number of iterations for the
            search.

        Returns:
        -----------------------------------------------------------------------
            Optional[List[RushHour]]: The solution path if found,
            None otherwise.
        """
        solution_path = []
        # calculate heuristic function of the starting state
        open_states = [HeapItem(self.total_cost_function(initial_state),\
                                initial_state)]
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

            # check if the game is won
            if current_state.is_solved():
                # reconstruct the path taken for the solution
                solution_path = self.reconstruct_path(current_state)
                print(current_state)
                # return the path
                return {'visited': iterations,
                        'solution': solution_path}
            
            # if no solution, add the current state to the closed states
            closed_states.add(current_state)
            
            # generate states to be visited, with option to generate look-ahead
            # states specified by depth
            future_states = current_state.generate_future_states(current_state,\
                                                                 depth=2)
            for state in future_states:
                # if a state is directly solvable, assign low cost to add to 
                # the front of the list
                if state.is_solvable():
                    heapq.heappush(open_states, HeapItem(-100, state))
                # check if state is not yet visited or in set with open states
                if state not in closed_states and state not in open_set:
                    # calculate cost of the state and add to the list
                    heapq.heappush(open_states,\
                        HeapItem(self.total_cost_function(state), state))
                    open_set.add(state)
                    
            iterations += 1
        # if no more states to be visited, return None
        print("No solution found")
        return None