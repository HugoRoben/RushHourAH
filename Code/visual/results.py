import matplotlib.pyplot as plt
import numpy as np

def visualize(stats, algo, save_to_file=False):
    times = stats['times']
    steps = stats['steps']


    if len(times) <= 1:
        print("\nNot enough data for visualization.")
        return

    fig, axs = plt.subplots(1, 2, figsize=(15, 7))

    log_times = np.log1p(times)
    num_bins_time = min(500, len(np.unique(log_times)))
    axs[0].hist(log_times, bins=num_bins_time, color='tab:blue', edgecolor='black')
    axs[0].set_title(f'{algo}: Time Taken (s)')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Frequency')

    # Histogram for steps
    num_bins_steps = min(500, len(np.unique(steps)))
    axs[1].hist(steps, bins=num_bins_steps, color='tab:red', edgecolor='black')
    axs[1].set_title(f'{algo}: Number of Steps')
    axs[1].set_xlabel('Steps')
    axs[1].set_ylabel('Frequency')

    plt.subplots_adjust(wspace=0.4)
    plt.suptitle(f'{algo} - Time Taken and Number of Steps', fontsize=16)

    if save_to_file:
        file_name = f'data/{algo}_test.png'
        plt.savefig(file_name)
        plt.close()
        print(f"Plot saved as {file_name}")
    # else:
    #     plt.show()


def format_stat(value):
        if isinstance(value, float):
            return f"{value:.3f}"
        return str(value)


def desc_stats(stats, unsolved_count, algo, save_to_file=False):
    times = stats['times']
    steps = stats['steps']
    visited = stats['visited']
    total_games = len(times)
    output = ""

    if total_games > 1:
        total_times = sum(times)
        total_steps = sum(steps)
        total_visited = sum(visited)
        solved = len(times)

        # Puzzle statistics
        output += f"\nPuzzle Statistics:\n{'-' * 25}\n"
        output += f"Total Puzzles  : {total_games}\n"
        output += f"Solved         : {solved}\n"
        output += f"Unsolved       : {unsolved_count}\n\n"

        # Time statistics
        output += f"\nTime Statistics:\n{'-' * 25}\n"
        output += f"Total Time     : {format_stat(total_times)}\n"
        output += f"Mean           : {format_stat(np.mean(times))}\n"
        output += f"Min            : {format_stat(np.min(times))}\n"
        output += f"Max            : {format_stat(np.max(times))}\n\n"

        # Steps statistics
        output += f"\nSteps Statistics:\n{'-' * 25}\n"
        output += f"Total Steps    : {format_stat(total_steps)}\n"
        output += f"Mean           : {format_stat(np.mean(steps))}\n"
        output += f"Min            : {format_stat(np.min(steps))}\n"
        output += f"Max            : {format_stat(np.max(steps))}\n"
        
        # Visited statistics
        output += f"\Visited states Statistics:\n{'-' * 36}\n"
        output += f"Total Steps               : {format_stat(total_visited)}\n"
        output += f"Mean                      : {format_stat(np.mean(visited))}\n"
        output += f"Min                       : {format_stat(np.min(visited))}\n"
        output += f"Max                       : {format_stat(np.max(visited))}\n"

    # When only one game is played
    else:
        solved_status = "Solved" if len(times) == 1 else "Unsolved"
        output += f"\nGame Statistics ({algo}):\n{'-' * 25}\n"
        output += f"Status         : {solved_status}\n"
        output += f"Time Taken (s) : {format_stat(times[0]) if times else 'N/A'}\n"
        output += f"Number of Steps: {format_stat(steps[0]) if steps else 'N/A'}\n"
        output += f"States visited : {format_stat(visited[0]) if visited else 'N/A'}\n"

    print(output)

    if save_to_file:
        file_name = f'data/{algo}_stats.txt'
        with open(file_name, 'w') as file:
            file.write(output)
        print(f"Statistics saved as {file_name}")

def plot_steps_histogram(steps, algo, save_to_file=False):
    num_bins = 42

    fig, ax = plt.subplots()

    # Histogram of the data
    n, bins, patches = ax.hist(steps, num_bins, density=False)

    # Calculate the mean of steps and add a vertical line at the mean
    mean_steps = sum(steps) / len(steps)
    ax.axvline(mean_steps, color='red', linestyle='dashed', linewidth=1)

    # Add a label for the mean line
    ax.text(mean_steps, max(n), f'    Mean: {mean_steps:.0f}', color='red', ha='left')

    ax.set_xlabel('Number of Steps')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{algo} - Histogram of Steps Taken')

    fig.tight_layout()

    if save_to_file:
        file_name = f'data/{algo}_steps_histogram.png'
        plt.savefig(file_name)
        plt.close()
        print(f"Histogram saved as {file_name}")
    else:
        plt.show()