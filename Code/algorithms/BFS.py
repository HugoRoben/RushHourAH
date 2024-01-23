from collections import deque
from .Astar import *


def breadth_first_search(RushGame, max_depth):
    """
    Perform a breadth-first search on a RushHour board to find solutions.
    
    Args:
        rush_hour_board (RushHour): The game board.
        max_depth (int, optional): Maximum search depth. Defaults to 25.

    Returns:
        dict: Contains visited states, solutions, and state counts per depth.
    """
    visited_states = set()
    solutions = []
    states_per_depth = {}

    visit_queue = deque()
    visit_queue.appendleft((RushGame, tuple()))  # Append the initial state and an empty path

    while len(visit_queue) != 0:
        current_board, path = visit_queue.pop()
        current_path = path + (current_board,)

        depth = len(current_path)  # The depth is the length of the path
        if depth > max_depth:
            break

        if current_board not in visited_states:
            visited_states.add(current_board)

            if current_board.is_solved():
                solutions.append(path + (current_board,))
                # solution = track_path(current_board)
                break  # or continue searching for all solutions
            else:
                for move in current_board.moves():
                    visit_queue.appendleft((move, path + (current_board,)))

    return {
        'visited': len(visited_states),
        'solutions': solutions,
        'depth_states': states_per_depth
    }


def solution_steps(solution_path):
    """
    Convert a solution path into a list of steps.

    Args:
        solution_path (tuple): The path of game states representing the solution.

    Returns:
        list: A list of steps to solve the puzzle.
    """
    steps = []
    for i in range(len(solution_path) - 1):
        current_state, next_state = solution_path[i], solution_path[i + 1]
        vehicle_current = list(current_state.vehicles - next_state.vehicles)[0]
        vehicle_next = list(next_state.vehicles - current_state.vehicles)[0]

        # Determine the direction of the vehicle's movement
        direction = determine_direction(vehicle_current, vehicle_next)
        steps.append(f'{vehicle_current.id}{direction}')

    return steps

def determine_direction(vehicle_current, vehicle_next):
    """
    Determine the direction of the vehicle's movement.

    Args:
        vehicle_prev (Vehicle): The vehicle in the previous state.
        vehicle_next (Vehicle): The vehicle in the next state.

    Returns:
        str: A single character representing the direction of movement.
    """
    if vehicle_current.x < vehicle_next.x:
        return 'R'  # Right
    elif vehicle_current.x > vehicle_next.x:
        return 'L'  # Left
    elif vehicle_current.y < vehicle_next.y:
        return 'D'  # Down
    elif vehicle_current.y > vehicle_next.y:
        return 'U'  # Up

