from GridObject import Grid
import CarObject
import csv
from Visualizer import Visualizer

if __name__ == "__main__":
    grid = Grid(6)
    grid.load_data('gameboards/Rushhour6x6_3.csv')
    Visualizer.draw(grid)

    output = [["car", "move"]]
    while True:
        print('Car,direction:')
        move_input = input()
        CarId = move_input.split(',')[0]
        steps = -int(move_input.split(',')[1])
        output.append([CarId,steps])

        grid.move_vehicle(CarId, int(steps))
        Visualizer.draw(grid)
    
        with open('output.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(output)

        if grid.is_solved(): 
            print("You won!")
            break


