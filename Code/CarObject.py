class vehicle:
    # initialize the car objects
    def __init__(self, CarId, orientation, col, row, length):
        # self.car_dict = {CarId, [orientation, col, row, length]}
        self._carid = CarId
        self._orientation = orientation
        self._x = col
        self._y = row
        self._length = length
        self.moves_history = {}

