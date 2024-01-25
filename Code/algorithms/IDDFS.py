from ..visual.visualizer import *
import matplotlib.pyplot as plt

def iterative_deepening_search(RushGame, max_depth=500):
    """
    Perform an iterative deepening depth-first search on a RushHour board to find solutions.

    Args:
        RushGame (RushHour): The game board.
        max_depth (int, optional): Maximum search depth. Defaults to 100.

    Returns:
        dict: Contains visited states, solutions, and state counts per depth.
    """
    for depth in range(1, max_depth + 1):
        visited = set()
        solution_path = depth_limited_search(RushGame, depth, visited)

        if solution_path is not None:
            visualizer = Visualizer(600, 600) 
            visualizer.animate_solution(solution_path)
            return {
                'solutions': [solution_path],
                'visited': len(visited),
                'depth_states': {depth: len(visited)}
            }
    return {'solutions': [], 'visited': 0, 'depth_states': {}, 'steps': 0}

def depth_limited_search(state, limit, visited, path=()):
    """
    Perform a depth-limited search from a given state.

    Args:
        state (RushHour): The current game state.
        limit (int): The depth limit for the search.
        path (tuple): The path taken to reach the current state.
        visited (set): Set of visited states.

    Returns:
        tuple: Visited states and the solution path, if found.
    """
    if state in visited:
        return None
    visited.add(state)

    if state.is_solved():

        return path + (state,)
    elif limit > 0:
        for move in state.moves():
            if move not in visited:
                new_path = depth_limited_search(move, limit - 1, visited, path + (state,))
                if new_path is not None:
                    return new_path
    return None


def solution_steps(solution_path):
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
    if vehicle_current.x < vehicle_next.x:
        return 'R'  # Right
    elif vehicle_current.x > vehicle_next.x:
        return 'L'  # Left
    elif vehicle_current.y < vehicle_next.y:
        return 'D'  # Down
    elif vehicle_current.y > vehicle_next.y:
        return 'U'  # Up