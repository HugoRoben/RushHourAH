from collections import deque


def breadth_first_search(RushGame, max_depth=100):
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
    visit_queue.appendleft((RushGame, tuple()))

    while len(visit_queue) != 0:
        current_board, path = visit_queue.pop()
        current_path = path + (current_board,)

        depth = len(current_path)
        if depth > max_depth:
            break

        if current_board not in visited_states:
            visited_states.add(current_board)

            states_per_depth[depth] = states_per_depth.get(depth, 0) + 1

            if current_board.is_solved():
                solutions.append(current_path)
                return {
                    'visited': len(visited_states),
                    'solutions': solutions,
                    'depth_states': states_per_depth
                }
            else:
                for move in current_board.moves():
                    visit_queue.appendleft((move, current_path))
    # print(f'{len(visited_states)} | {states_per_depth}')
    # return {
    #     'visited': len(visited_states),
    #     'solutions': solutions,
    #     'depth_states': states_per_depth
    # }

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





# def breadth_first_search(r, max_depth=25):
#     """
#     Find solutions to given RushHour board using breadth first search.
#     Returns a dictionary with named fields:
#         visited: the number of configurations visited in the search
#         solutions: paths to the goal state
#         depth_states: the number of states visited at each depth

#     Arguments:
#         r: A RushHour board.

#     Keyword Arguments:
#         max_depth: Maximum depth to traverse in search (default=25)
#     """
#     visited = set()
#     solutions = list()
#     depth_states = dict()

#     queue = deque()
#     queue.appendleft((r, tuple()))
#     while len(queue) != 0:
#         board, path = queue.pop()
#         new_path = path + tuple([board])

#         depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1

#         if len(new_path) >= max_depth:
#             break

#         if board in visited:
#             continue
#         else:
#             visited.add(board)

#         if board.is_solved():
#             solutions.append(new_path)
#         else:
#             queue.extendleft((move, new_path) for move in board.moves())

#     return {'visited': visited,
#             'solutions': solutions,
#             'depth_states': depth_states}

# def solution_steps(solution):
#     """Generate list of steps from a solution path."""
#     steps = []
#     for i in range(len(solution) - 1):
#         r1, r2 = solution[i], solution[i+1]
#         v1 = list(r1.vehicles - r2.vehicles)[0]
#         v2 = list(r2.vehicles - r1.vehicles)[0]
#         if v1.x < v2.x:
#             steps.append('{0}R'.format(v1.id))
#         elif v1.x > v2.x:
#             steps.append('{0}L'.format(v1.id))
#         elif v1.y < v2.y:
#             steps.append('{0}D'.format(v1.id))
#         elif v1.y > v2.y:
#             steps.append('{0}U'.format(v1.id))
#     return steps
