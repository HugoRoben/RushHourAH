import random
from Code.classes.RushClass import RushHour
# import time
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd


def solve_puzzle(Rush_game, max_iterations=1000000):
    game = Rush_game
    move_count = 0
    for _ in range(max_iterations):
        if game.is_solved():
            return game, move_count

        possible_moves = list(game.moves())
        if not possible_moves:
            return None
        next_state = random.choice(possible_moves)
        
        if next_state is None:  # or hash(next_state) in self.visited_states
            print("No more moves available or state repeated.")
            break
        
        # self.visited_states.add(hash(next_state))
        move_count += 1
        game = next_state  # Update the game state
    return 0
