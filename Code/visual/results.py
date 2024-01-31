import matplotlib.pyplot as plt
import numpy as np

def format_stat(value):
    """
    Format a statistical value to a string with 3 decimal places if it's a float.

    Args:
    ---------------------------------------------------------------------------
        value (Union[float, int]): The value to format.

    Returns:
    ---------------------------------------------------------------------------
        str: The formatted value as a string.
    """
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)

def desc_stats(stats, unsolved_count, algo, save_to_file=False):
    """
    Describe the statistics of puzzle solving attempts, including times, steps, 
        and visited states.

    Args:
    ---------------------------------------------------------------------------
        stats (Dict[str, List[Union[float, int]]]): A dictionary containing 
            'times', 'steps', and 'visited' data.
        unsolved_count (int): The number of puzzles that were not solved.
        algo (str): The name of the algorithm used for the statistics.
        save_to_file (bool, optional): Flag to determine if the statistics
            should be saved to a file. Defaults to False.
    """
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
        file_name = f'data/{algo}_stats_9_4_depth2.txt'
        with open(file_name, 'w') as file:
            file.write(output)
        print(f"Statistics saved as {file_name}")

def plot_steps_histogram(steps, algo, save_to_file=False):
    """
    Plot a histogram of the number of steps taken to solve puzzles for a given algorithm.

    Args:
    ----------------------------------------------------------------------------
        steps (List[int]): A list of the number of steps taken for each puzzle.
        algo (str): The name of the algorithm used for the statistics.
        save_to_file (bool, optional): Flag to determine if the histogram should 
            be saved to a file. Defaults to False.
    """
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
        file_name = f'data/{algo}_steps_9_4_depth1.png'
        plt.savefig(file_name)
        plt.close()
        print(f"Histogram saved as {file_name}")
    else:
        plt.show()