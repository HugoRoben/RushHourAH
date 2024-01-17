from collections import deque


def breadth_first_search(r, max_depth=25):
    """
    Find solutions to given RushHour board using breadth first search.
    Returns a dictionary with named fields:
        visited: the number of configurations visited in the search
        solutions: paths to the goal state
        depth_states: the number of states visited at each depth

    Arguments:
        r: A RushHour board.

    Keyword Arguments:
        max_depth: Maximum depth to traverse in search (default=25)
    """
    visited = set()
    solutions = list()
    depth_states = dict()

    queue = deque()
    queue.appendleft((r, tuple()))
    while len(queue) != 0:
        board, path = queue.pop()
        new_path = path + tuple([board])

        depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1

        if len(new_path) >= max_depth:
            break

        if board in visited:
            continue
        else:
            visited.add(board)

        if board.is_solved():
            solutions.append(new_path)
        else:
            queue.extendleft((move, new_path) for move in board.moves())

    return {'visited': visited,
            'solutions': solutions,
            'depth_states': depth_states}

def solution_steps(solution):
    """Generate list of steps from a solution path."""
    steps = []
    for i in range(len(solution) - 1):
        r1, r2 = solution[i], solution[i+1]
        v1 = list(r1.vehicles - r2.vehicles)[0]
        v2 = list(r2.vehicles - r1.vehicles)[0]
        if v1.x < v2.x:
            steps.append('{0}R'.format(v1.id))
        elif v1.x > v2.x:
            steps.append('{0}L'.format(v1.id))
        elif v1.y < v2.y:
            steps.append('{0}D'.format(v1.id))
        elif v1.y > v2.y:
            steps.append('{0}U'.format(v1.id))
    return steps
