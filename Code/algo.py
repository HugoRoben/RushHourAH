# Importeer de benodigde klassen
from GridObject import Grid
from CarObject import vehicle
from Visualizer import Visualizer
import random
import csv
import matplotlib.pyplot as plt

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

    def solve_puzzle(self, max_iterations=1000000):
        for _ in range(max_iterations):
            car_id, steps = self.generate_random_move()
            self.grid.move_vehicle(car_id, steps)

            self.output.append([car_id,steps])
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
        return self.count


if __name__ == "__main__":
    results_list = []
    # Visualizer.setup_interactive_mode()
    for i in range(100):

        solver = RushHourSolver(6, 'gameboards/Rushhour6x6_3.csv')
        results_list.append(solver.solve_puzzle())

    plt.hist(results_list, bins = 30)
    plt.show()
    # Visualizer.close_interactive_mode()
