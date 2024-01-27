from collections import deque
from ..visual.visualizer import *
import matplotlib.pyplot as plt


def iterative_deepening_search(RushGame, max_depth=500):
    states_per_depth = {}
    solution = None

    for depth in range(1, max_depth + 1):
        visited_states = set()
        visit_queue = deque([(RushGame, ())])

        while visit_queue:
            current_board, path = visit_queue.pop()

            if current_board in visited_states and len(path) < depth:
                continue

            visited_states.add(current_board)
            new_path = path + (current_board,)

            if current_board.is_solved():
                solution = new_path
                break

            if len(new_path) < depth:
                for move in current_board.moves():
                    visit_queue.appendleft((move, new_path))

        states_per_depth[depth] = len(visited_states)
        if solution:
            break

    total_visited = sum(states_per_depth.values())
    return {
        'visited': total_visited,
        'solution': solution,
        'depth_states': states_per_depth
    }
