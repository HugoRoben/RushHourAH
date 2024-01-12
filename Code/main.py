from GridObject import Grid
import CarObject
from Visualizer import Visualizer

if __name__ == "__main__":
    grid = Grid(6)
    grid.load_data('gameboards/Rushhour6x6_1.csv')  # Adjusted to a valid file path
    Visualizer.draw(grid)

    while True:
        CarId = input("Which car: ")
        steps = input("What direction do you want to move: ")

        grid.move_vehicle(CarId, int(steps))
        Visualizer.draw(grid)


# red_car = CarObject.vehicle('H', 2, 2, 2)
# grid.add_vehicle(red_car)
# grid.add_vehicle(CarObject.vehicle('V', 0, 0, 2))
# grid.add_vehicle(CarObject.vehicle('V', 3, 3, 3))



# # Example move

