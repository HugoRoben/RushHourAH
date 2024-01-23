import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

def visualize(data, unsolved_count):
    times = [data[key]['time'] for key in data if 'time' in data[key]]
    steps = [data[key]['steps'] for key in data if 'steps' in data[key] and data[key]['steps'] is not None]

    if not times or not steps:
        print("No data for visualization available.")
        return
    
    num_bins = 25

    # Set up the figure and axes
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Histogram for time
    axs[0].hist(times, bins=num_bins, color='tab:blue', edgecolor='black')
    axs[0].set_title('Time Taken (s)')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Frequency')

    # Histogram for steps
    axs[1].hist(steps, bins=num_bins, color='tab:red', edgecolor='black')
    axs[1].set_title('Number of Steps')
    axs[1].set_xlabel('Steps')

    # Solve statistics
    solved = len(times)
    unsolved = unsolved_count
    total = solved + unsolved
    
    # Time statistics
    stats_time = {'Mean': np.mean(times),
                  'Median': np.median(times),
                  'Std Dev': np.std(times),
                  'Min': np.min(times),
                  'Max': np.max(times)}
    
    # Steps statistics
    stats_steps = {'Mean': np.mean(steps),
                   'Median': np.median(steps),
                   'Std Dev': np.std(steps),
                   'Min': np.min(steps),
                   'Max': np.max(steps)}
    
    # Add some spacing between the histograms
    plt.subplots_adjust(wspace=0.3)

    plt.suptitle('Comparison of Time Taken and Number of Steps')
    plt.show()
    desc_stats(stats_time, stats_steps, total, solved, unsolved)



def desc_stats(stats_time, stats_steps, total, solved_count, unsolved_count, save_to_file=False, filename="stats.txt"):
    headers = ["Type", "Total", "Solved", "Unsolved"] + list(stats_time.keys())
    data = [
        ["Time"] + [total, solved_count, unsolved_count] + list(stats_time.values()),
        ["Steps"] + [total, solved_count, unsolved_count] + list(stats_steps.values())
    ]

    # Create the table
    table = tabulate(data, headers=headers, tablefmt="grid")

    # Print the table to console
    print(table)

    # Save to text file if required
    if save_to_file:
        with open(filename, 'w') as file:
            file.write(table)


# Example usage
# stats_time = {'Mean': 10, 'Median': 5, 'Std Dev': 2, 'Min': 1, 'Max': 15}
# stats_steps = {'Mean': 20, 'Median': 10, 'Std Dev': 4, 'Min': 2, 'Max': 30}

# desc_stats(stats_time, stats_steps)


