from ..classes.VehicleClass import Vehicle
from ..classes.RushClass import *
import heapq

def heuristic(state):
    for vehicle in state.vehicles:
        if vehicle.id == 'X':  # Assuming 'X' is the red car
            return state.dim_board - (vehicle.x + vehicle.length)
    return float('inf')

def astar_search(initial_state, goal_state):
    # Priority queues for open states (using heapq for efficiency)
    open_start = [(heuristic(initial_state), initial_state)]
    open_goal = [(heuristic(goal_state), goal_state)]

    # Sets for closed states
    closed_start, closed_goal = set(), set()

    # Backtrack dictionaries to reconstruct paths
    backtrack_start, backtrack_goal = {}, {}

    while open_start and open_goal:
        # Get the state with the lowest F-value from each direction
        # _, makes the code only pop the state, not the heuristic value
        _, current_start = heapq.heappop(open_start)
        _, current_goal = heapq.heappop(open_goal)

        # Check if we've found a meeting point
        if current_start == current_goal or current_start in closed_goal or current_goal in closed_start:
            return reconstruct_path(backtrack_start, backtrack_goal, current_start, current_goal)

        # Add current states to closed sets
        closed_start.add(current_start)
        closed_goal.add(current_goal)

        # Expand states in both directions
        for next_state in current_start.moves():
            if next_state not in closed_start:
                heapq.heappush(open_start, (heuristic(next_state) + next_state.move_count, next_state))
                backtrack_start[next_state] = current_start

        for next_state in current_goal.moves():
            if next_state not in closed_goal:
                heapq.heappush(open_goal, (heuristic(next_state) + next_state.move_count, next_state))
                backtrack_goal[next_state] = current_goal

    return None  # No solution found

def reconstruct_path(backtrack_start, backtrack_goal, meeting_start, meeting_goal):
    # Reconstruct path from start to meeting point
    path_start = []
    while meeting_start in backtrack_start:
        path_start.append(meeting_start)
        meeting_start = backtrack_start[meeting_start]

    # Reconstruct path from goal to meeting point
    path_goal = []
    while meeting_goal in backtrack_goal:
        path_goal.append(meeting_goal)
        meeting_goal = backtrack_goal[meeting_goal]

    return path_start[::-1] + path_goal






