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
            return move_count

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


# def plot_combined_statistics(file_stats):
#     all_times = []
#     all_moves = []
#     labels = []

#     for file, stats in file_stats.items():
#         all_times.extend(stats["times"])
#         all_moves.extend(stats["moves"])
#         labels.extend([os.path.basename(file)] * len(stats["times"]))

#     data = pd.DataFrame({
#         'Time': all_times,
#         'Moves': all_moves,
#         'File': labels
#     })

#     plt.figure(figsize=(12, 6))

#     plt.subplot(1, 2, 1)
#     sns.boxplot(x='File', y='Time', data=data)
#     plt.xticks(rotation=45)
#     plt.title("Time Taken for Each File")
#     plt.ylabel("Time (seconds)")

#     plt.subplot(1, 2, 2)
#     sns.boxplot(x='File', y='Moves', data=data)
#     plt.xticks(rotation=45)
#     plt.title("Move Counts for Each File")
#     plt.ylabel("Number of Moves")

#     plt.tight_layout()
#     plt.show()

# def calculate_statistics(times, move_counts):
#     avg_time = sum(times) / len(times)
#     avg_moves = sum(move_counts) / len(move_counts)
#     max_time = max(times)
#     min_time = min(times)
#     max_moves = max(move_counts)
#     min_moves = min(move_counts)

#     return {
#         "average_time": avg_time,
#         "average_moves": avg_moves,
#         "max_time": max_time,
#         "min_time": min_time,
#         "max_moves": max_moves,
#         "min_moves": min_moves
#     }