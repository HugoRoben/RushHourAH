from collections import deque
from ..classes.RushClass import RushHour
from typing import Union, Dict, List

def breadth_first_search(RushGame: RushHour, max_depth: int =100)\
    -> Dict[str, Union[int, List[RushHour], Dict[int, List[RushHour]]]]:
    """
    Perform a breadth-first search to solve the Rush Hour puzzle.

    Args:
    ---------------------------------------------------------------------------
        RushGame (RushGame): An instance of the Rush Hour puzzle game, which 
            should have methods is_solved and moves.
        max_depth (int): The maximum depth to search in the puzzle.

    Returns:
    ---------------------------------------------------------------------------
        Dict[str, Union[int, List[RushHour], Dict[int, List[RushHour]]]]: A 
        dictionary including the number of visited states, the solution 
        (if found), and states visited per depth level.
    """
    
    visited_states = set()
    states_per_depth = {}

    visit_queue = deque()
    # add the intitial state to the visit_que
    visit_queue.appendleft((RushGame, tuple()))

    while len(visit_queue) != 0:
        current_state, path = visit_queue.pop()
        current_path = path + (current_state,)

        depth = len(current_path)
        if depth > max_depth:
            break
        
        # check if the state is not already seen
        if current_state not in visited_states:
            # add the state to visited states
            visited_states.add(current_state)

            if current_state.is_solved():
                solution = current_path
                break
            else:
                # add all possible moves from the state to the queue
                for move in current_state.moves():
                    visit_queue.appendleft((move, path + (current_state,)))
    return {
        'visited': len(visited_states),
        'solution': solution,
        'depth_states': states_per_depth
    }

# To get a deeper understanding on what happens at each move, we can keep track of the 
# steps taken at each move with the following code:
#
# def track_path(end_state):
#     current_board = end_state
#     path = []
#     while current_board is not None:
#         path.insert(0, current_board)
#         current_board = current_board.parent
#     return path

# def solution_steps(solution_path):
#     """
#     Convert a solution path into a list of steps.

#     Args:
#         solution_path (tuple): The path of game states representing the solution.

#     Returns:
#         list: A list of steps to solve the puzzle.
#     """
#     steps = []
#     for i in range(len(solution_path) - 1):
#         current_state, next_state = solution_path[i], solution_path[i + 1]
#         vehicle_current = list(current_state.vehicles - next_state.vehicles)[0]
#         vehicle_next = list(next_state.vehicles - current_state.vehicles)[0]

#         # Determine the direction of the vehicle's movement
#         direction = determine_direction(vehicle_current, vehicle_next)
#         steps.append(f'{vehicle_current.id}{direction}')

#     return steps


# def determine_direction(vehicle_current, vehicle_next):
#     """
#     Determine the direction of the vehicle's movement.

#     Args:
#         vehicle_prev (Vehicle): The vehicle in the previous state.
#         vehicle_next (Vehicle): The vehicle in the next state.

#     Returns:
#         str: A single character representing the direction of movement.
#     """
#     if vehicle_current.x < vehicle_next.x:
#         return 'R'  # Right
#     elif vehicle_current.x > vehicle_next.x:
#         return 'L'  # Left
#     elif vehicle_current.y < vehicle_next.y:
#         return 'D'  # Down
#     elif vehicle_current.y > vehicle_next.y:
#         return 'U'  # Up
