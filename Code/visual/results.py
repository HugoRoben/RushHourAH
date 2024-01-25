import matplotlib.pyplot as plt
import numpy as np


def visualize(steps, times, algo, save_to_file=True):
    if not times or not steps:
        print("No data for visualization available.")
        return

    num_bins = 50000
    title_name = algo
    file_name = f'data/{title_name}.png'

    # Set up the figure and axes
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Histogram for time
    axs[0].hist(times, bins=num_bins, color='tab:blue', edgecolor='black')
    axs[0].set_title(f'{title_name}: Time Taken (s)')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Frequency')

    # Histogram for steps
    axs[1].hist(steps, bins=num_bins, color='tab:red', edgecolor='black')
    axs[1].set_title(f'{title_name}: Number of Steps')
    axs[1].set_xlabel('Steps')

    # Add some spacing between the histograms
    plt.subplots_adjust(wspace=0.3)

    # Global title
    plt.suptitle(f'{title_name} - Comparison of Time Taken and Number of Steps')


    if save_to_file:
        plt.savefig(file_name)
        plt.close()
        print(f"Plot saved as {file_name}")
    else:
        plt.show()


def desc_stats(steps, times, unsolved_count, algo, save_to_file=True):
    file_name = f'data/{algo}.txt'
    
    total_times = sum(times)
    total_steps = sum(steps)
    
    solved = len(times)
    unsolved = unsolved_count
    total = solved + unsolved

    def format_stat(value):
        if isinstance(value, float):
            return f"{value:.3f}"
        return str(value)

    # Puzzle statistics
    stats_puzzle = f"\nPuzzle Statistics:\n{'-' * 25}\n"
    stats_puzzle += f"Total Puzzles  : {total}\n"
    stats_puzzle += f"Solved         : {solved}\n"
    stats_puzzle += f"Unsolved       : {unsolved}\n\n"

    # Time statistics
    stats_time = f"\nTime Statistics:\n{'-' * 25}\n"
    stats_time += f"Total Time     : {format_stat(total_times)}\n"
    stats_time += f"Mean           : {format_stat(np.mean(times))}\n"
    stats_time += f"Min            : {format_stat(np.min(times))}\n"
    stats_time += f"Max            : {format_stat(np.max(times))}\n\n"

    # Steps statistics
    stats_steps = f"\nSteps Statistics:\n{'-' * 25}\n"
    stats_steps += f"Total Steps    : {format_stat(total_steps)}\n"
    stats_steps += f"Mean           : {format_stat(np.mean(steps))}\n"
    stats_steps += f"Min            : {format_stat(np.min(steps))}\n"
    stats_steps += f"Max            : {format_stat(np.max(steps))}\n"

    # Combine all statistics
    output = stats_puzzle + stats_time + stats_steps
    print(output)

    # Save to text file if required
    if save_to_file:
        with open(file_name, 'w') as file:
            file.write(output)
