from ..classes.VehicleClass import Vehicle
from ..classes.RushClass import *
import heapq

def calculate_cost(current_board, dimension):
    Blocking_cars_cost = 0

    # Directly access the target vehicle 'X'
    vehicle_x = next((v for v in current_board.vehicles if v.id == 'X'), None)
    if not vehicle_x:
        return float('inf')  # 'X' not found, return a high cost

    # Calculate distance to exit
    distance_to_exit = dimension - vehicle_x.x - vehicle_x.length

    # Check for blocking vehicles
    for vehicle in current_board.vehicles:
        if vehicle.y == vehicle_x.y and vehicle.x > vehicle_x.x + vehicle_x.length - 1:
            # A vehicle is blocking if it's in the same row and to the right of 'X'
            Blocking_cars_cost += 1

    total_cost = Blocking_cars_cost + distance_to_exit
    return total_cost

import itertools

def sort_states_by_cost(states, dimension):
    # Create a list to store the state-cost pairs
    states_with_cost = []
    # Counter for unique identifiers
    unique_id = itertools.count()

    # Calculate cost for each state and add it to the heap
    for state in states:
        cost = calculate_cost(state[0], dimension)
        heapq.heappush(states_with_cost, (cost, next(unique_id), state[0]))

    # Extract the top 100 states with the lowest cost
    top_states = [heapq.heappop(states_with_cost)[2] for _ in range(min(1000, len(states_with_cost)))]

    return top_states





