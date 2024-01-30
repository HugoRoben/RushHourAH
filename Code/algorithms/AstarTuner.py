from .Astar import *
import time

def solve_parameters(rush_game):
    # blocker depth
    for i in range(2,4):
        # look ahead states
        for j in range(1,3):
            # blocker_weight
            for k in range(1, 4):
                # length weight
                for l in range(1,4):
                    # distance weight
                    for m in range(-2, 2):
                        start_time = time.perf_counter()
                        results = Astar(rush_game, k, l, j, i, m).astar_search(rush_game)