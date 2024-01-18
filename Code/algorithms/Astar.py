class HeapItem:
    def __init__(self, priority, rush_hour_obj):
        self.priority = priority
        self.rush_hour_obj = rush_hour_obj

    def __lt__(self, other):
        return self.priority < other.priority
    
from ..classes.VehicleClass import Vehicle
from ..classes.RushClass import *
import heapq

# def heuristic(state):
#     for vehicle in state.vehicles:
#         if vehicle.id == 'X':  # Assuming 'X' is the red car
#             return state.dim_board - (vehicle.x + vehicle.length)
#     return float('inf')

def heuristic(state1, state2):
    """
    Calculate the number of differing vehicles between two states.
    
    Args:
    state1, state2 (RushHour): Two instances of the RushHour game state.

    Returns:
    int: The number of vehicles that differ between the two states.
    """
    # Ensure both states have the same number of vehicles
    if len(state1.vehicles) != len(state2.vehicles):
        raise ValueError("States do not have the same number of vehicles.")

    # Count the number of vehicles that are different
    differing_vehicles = sum(1 for v1, v2 in zip(state1.vehicles, state2.vehicles) if v1 != v2)
    return differing_vehicles

def is_winning_state(state):
    """
    Check if the 'X' vehicle (red car) can exit the board.
    """
    for vehicle in state.vehicles:
        if vehicle.id == 'X':
            # Check if the red car's path to the exit is clear
            for x in range(vehicle.x + 1, state.dim_board):
                if any(v.x == x and v.y == vehicle.y -1 or v.y == vehicle.y - 2 for v in state.vehicles if v.id != 'X'):
                    # Found another car blocking the path
                    return False
            return True
    return False

def astar_search(initial_state, goal_state, max_iterations=10000):
    open_start = [HeapItem(heuristic(initial_state, goal_state), initial_state)]
    open_goal = [HeapItem(heuristic(goal_state, initial_state), goal_state)]

    closed_start, closed_goal = set(), set()
    backtrack_start, backtrack_goal = {}, {}

    iterations = 0

    while open_start and open_goal:
        if iterations >= max_iterations:
            print("Maximum iterations reached, terminating search.")
            break

        current_start = heapq.heappop(open_start).rush_hour_obj
        current_goal = heapq.heappop(open_goal).rush_hour_obj

        print(f"Current Goal State: {current_start}")

        if is_winning_state(current_start):
            print("Winning state found")
            return reconstruct_path(backtrack_start, {}, current_start, None)


        if current_start == current_goal or current_start in closed_goal or current_goal in closed_start:
            print("Meeting point found")
            return reconstruct_path(backtrack_start, backtrack_goal, current_start, current_goal)

        closed_start.add(current_start)
        closed_goal.add(current_goal)

        for next_state in current_start.moves():
            if next_state not in closed_start:
                heapq.heappush(open_start, HeapItem(heuristic(next_state, current_goal) + next_state.move_count, next_state))
                backtrack_start[next_state] = current_start

        for next_state in current_goal.moves():
            if next_state not in closed_goal:
                heapq.heappush(open_goal, HeapItem(heuristic(next_state, current_start) + next_state.move_count, next_state))
                backtrack_goal[next_state] = current_goal

        iterations += 1
        # print(f"Open Start Size: {len(open_start)}, Open Goal Size: {len(open_goal)}, Iteration: {iterations}")

    print("No solution found")
    return None

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




# F,H,1,4,2
# G,V,3,3,2
# H,H,4,4,2
# I,V,6,3,2
# J,H,5,5,2
# K,V,1,5,2
# L,V,3,5,2
# E,V,4,2,2