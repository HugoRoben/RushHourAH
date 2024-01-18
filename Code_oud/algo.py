# Importeer de benodigde klassen
from GridObject import Grid
from CarObject import vehicle
from Visualizer import Visualizer
import random
import csv
import matplotlib.pyplot as plt
import glob
import os
import seaborn as sns
import pandas as pd
import time

#new1-joeri-: 211 sec, 150 keer alle borden
#new1-joeri-: 17.15 sec, 15 keer alle borden
#new0-joeri-: 20.5 sec, 15 keer alle borden
#oud-hugo: 20.6 sec, 15 keer alle borden

class RushHourSolver:
    def __init__(self, grid_size, gameboard_file):
        self.output = [["car", "move"]]
        self.count = 0
        self.grid = Grid(grid_size)
        self.grid.load_data(gameboard_file)

        self.result_list = []
    

    def generate_random_move(self):
        vehicle = random.choice(list(self.grid.vehicle_dict))
        steps = random.choice([-1, 1]) # Aanpassen aan de maximale stapgrootte
        return vehicle, steps

    def solve_puzzle(self, max_iterations=150000000):
        for _ in range(max_iterations):
            car_id, steps = self.generate_random_move()
            self.grid.move_vehicle(car_id, steps)

            # self.output.append([car_id,steps])
            self.count +=1
            
            # Visualizer.draw(self.grid)  # Optioneel, voor visualisatie
            if self.grid.is_solved():
                # with open('output.csv', 'w', newline='') as file:
                #     writer = csv.writer(file)
                #     writer.writerows(self.output)
                # print(f"'aantal stappen:' {self.count}")
                # print("Puzzel opgelost!")
                return self.count
        # print("Geen oplossing gevonden binnen de limiet van iteraties.")
        return 0

if __name__ == "__main__":
    solutions_dict = {}
    start_time = time.time()
    
    # Loop over CSV files in the gameboards directory
    for csv_file in glob.glob('gameboards/*.csv'):
        gameboard_name = os.path.basename(csv_file).split('.')[0]  # Extract the gameboard name from the file path
        gameboard_file = csv_file

        # Extracting size
        size_part = gameboard_name.split('_')[0]  # Assuming format "Rushhour<size>_<other>"
        size = int(size_part.replace('Rushhour', '').split('x')[0])

        # Print the size for debugging
        # print(f"Processing {gameboard_name}: Grid size = {size}")

        number_of_steps = []

        for _ in range(10):
            solver = RushHourSolver(size, gameboard_file)
            count = solver.solve_puzzle()
            number_of_steps.append(count)
        
        solutions_dict[gameboard_name] = number_of_steps

    end_time = time.time()

    # Calculate the total execution time
    total_time = end_time - start_time
    print(f"Total execution time: {total_time} seconds")
    
    gameboards = []
    steps = []
    for gameboard, step_counts in solutions_dict.items():
        gameboards.extend([gameboard] * len(step_counts))
        steps.extend(step_counts)

    # Create a dataframe
    data = pd.DataFrame({'Gameboard': gameboards, 'Steps': steps})

    # Create a boxplot
    plt.figure(figsize=(12, 8))

    # Boxplot
    sns.boxplot(data=data, x='Gameboard', y='Steps', palette="Set2")

    # Adding scatterplot
    sns.stripplot(data=data, x='Gameboard', y='Steps', color='black', alpha=0.5, jitter=True)

    # Customizing plot
    plt.xlabel('Gameboard')
    plt.ylabel('Number of Steps')
    plt.title('Boxplot and Scatterplot of Steps to Solve Rush Hour Puzzles per Gameboard')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.show()


    stats_data = []
    for gameboard, steps in solutions_dict.items():
        gameboard_data = pd.Series(steps)
        stats = {
            'Gameboard': gameboard,
            'Mean': gameboard_data.mean(),
            'Median': gameboard_data.median(),
            'Min': gameboard_data.min(),
            'Max': gameboard_data.max(),
            'Std': gameboard_data.std()
        }
        stats_data.append(stats)

    descriptive_stats_df = pd.DataFrame(stats_data)

    print(descriptive_stats_df)
