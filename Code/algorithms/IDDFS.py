from collections import deque
from ..classes.RushClass import RushHour
from typing import Union, Dict, List

def iterative_deepening_search(RushGame: RushHour, max_depth: int=500)\
    -> Dict[str, Union[int, List[RushHour], Dict[int, List[RushHour]]]]:
    """
    Performs an iterative deepening search on the Rush Hour game.

    Args:
    ---------------------------------------------------------------------------
        RushGame (RushGame): An instance of the Rush Hour game.
        max_depth (int, optional): The maximum depth for the search. Defaults to 500.

    Returns:
    ---------------------------------------------------------------------------
        Dict[str, Union[int, List[RushHour], Dict[int, List[RushHour]]]]:
        A dictionary the total visited states, the solution (if found), and 
        states per depth.
    """
    
    states_per_depth = {}
    solution = None

    # Iterate over a range of depth levels
    for depth in range(1, max_depth + 1):
        visited_states = set()
        visit_queue = deque([(RushGame, ())])

        # Loop until there are no states left to visit or a solution is found
        while visit_queue:
            current_board, path = visit_queue.pop()
        
            if current_board in visited_states and len(path) < depth:
                continue

            visited_states.add(current_board)
            new_path = path + (current_board,)

            # Check if the current state is a solution
            if current_board.is_solved():
                solution = new_path
                break
            
            # If the path is not yet at maximum depth, extend the search
            if len(new_path) < depth:
                for move in current_board.moves():
                    visit_queue.appendleft((move, new_path))

        states_per_depth[depth] = len(visited_states)
        if solution:
            break

    total_visited = sum(states_per_depth.values()) # Calculate the total number of visited states
    return {
        'visited': len(visited_states),
        'solution': solution,
        'depth_states': states_per_depth
    }
