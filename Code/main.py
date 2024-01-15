from GridObject import Grid
import CarObject
import csv
from Visualizer import Visualizer


if __name__ == "__main__":
    """
    Main function to run the Rush Hour game.

    Initializes the game grid, loads the game data, and enters a loop
    allowing the player to make moves. Records moves to an output file.
    The game continues until the puzzle is solved.

    Preconditions:
        - The 'gameboards/Rushhour6x6_1.csv' file should exist and be correctly formatted.
        - The Visualizer module should be able to correctly draw the game grid.

    Postconditions:
        - The game is executed, allowing user interaction.
        - Moves are recorded and saved to 'output.csv'.
        - Continues until the puzzle is solved.
    """
    grid = Grid(6)
    grid.load_data('gameboards/Rushhour6x6_3.csv')
    Visualizer.draw(grid)

    output = [["car", "move"]]
    while True:
        print('Car,direction:')
        move_input = input()
        CarId = move_input.split(',')[0]
        steps = move_input.split(',')[1]
        output.append([CarId,steps])

        grid.move_vehicle(CarId, int(steps))
        Visualizer.draw(grid)
    
        with open('output.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(output)

        if grid.is_solved(): 
            print("You won!")
            break
