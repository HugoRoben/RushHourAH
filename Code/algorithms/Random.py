import random
from ..classes.RushClass import *# import time
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd


def solve_puzzle(Rush_game, max_iterations=1000000):
    game = Rush_game
    move_count = 0
    for _ in range(max_iterations):
        if game.is_solved():
            print(move_count)
            print(game)
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

# # Create a dataframe
#     data = pd.DataFrame({'Gameboard': gameboards, 'Steps': steps})

#     # Create a boxplot
#     plt.figure(figsize=(12, 8))

#     # Boxplot
#     sns.boxplot(data=data, x='Gameboard', y='Steps', palette="Set2")

#     # Adding scatterplot
#     sns.stripplot(data=data, x='Gameboard', y='Steps', color='black', alpha=0.5, jitter=True)

#     # Customizing plot
#     plt.xlabel('Gameboard')
#     plt.ylabel('Number of Steps')
#     plt.title('Boxplot and Scatterplot of Steps to Solve Rush Hour Puzzles per Gameboard')
#     plt.xticks(rotation=45)
#     plt.grid(True)
#     plt.tight_layout()

#     plt.show()


#     stats_data = []
#     for gameboard, steps in solutions_dict.items():
#         gameboard_data = pd.Series(steps)
#         stats = {
#             'Gameboard': gameboard,
#             'Mean': gameboard_data.mean(),
#             'Median': gameboard_data.median(),
#             'Min': gameboard_data.min(),
#             'Max': gameboard_data.max(),
#             'Std': gameboard_data.std()
#         }
#         stats_data.append(stats)

#     descriptive_stats_df = pd.DataFrame(stats_data)

#     print(descriptive_stats_df)