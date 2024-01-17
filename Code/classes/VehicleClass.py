class Vehicle(object):
    """A configuration of a single vehicle."""
    def __init__(self, id, orientation, x, y,  length):
        self.id = id
        self.orientation = orientation
        self.x = x
        self.y = y
        self.length = length
        
        # if 0 <= x <= 5:
        #     self.x = x
        # else:
        #     raise ValueError('Invalid x {0}'.format(x))

        # if 0 <= y <= 5:
        #     self.y = y
        # else:
        #     raise ValueError('Invalid y {0}'.format(y))
        
        # if 2 <= length <= 3:
        #     self.length = length
        # else:
        #     raise ValueError('Invalid length {0}'.format(length))
        
        # if orientation == 'H':
        #     self.orientation = orientation
        #     x_end = self.x + (self.length - 1)
        #     y_end = self.y
        # elif orientation == 'V':
        #     self.orientation = orientation
        #     x_end = self.x
        #     y_end = self.y + (self.length - 1)
        # else:
        #     raise ValueError('Invalid orientation {0}'.format(orientation))

        # if x_end > 5 or y_end > 5:
        #     raise ValueError('Invalid configuration')
        
        def __hash__(self):
            return hash(self.__repr__())

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __ne__(self, other):
            return not self.__eq__(other)

        def __repr__(self):
            return "Vehicle({0}, {1}, {2}, {3})".format(self.id, self.orientation, self.x, self.y)