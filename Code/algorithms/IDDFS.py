from collections import deque
from ..classes.RushClass import RushHour

def iterative_deepening_search(RushGame: RushHour, max_depth: int=500):
    """
    Performs an iterative deepening search on the Rush Hour game.

    Args:
    ---------------------------------------------------------------------------
        RushGame (RushGame): An instance of the Rush Hour game.
        max_depth (int, optional): The maximum depth for the search. Defaults to 500.

    Returns:
    ---------------------------------------------------------------------------
        Dict[str, any]: A dictionary containing the search statistics, including 
        the total visited states, the solution (if found), and states per depth.
    """
    
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
        'visited': len(visited_states),
        'solution': solution,
        'depth_states': states_per_depth
    }
