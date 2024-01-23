class Vehicle(object):
    """A configuration of a single vehicle."""
    def __init__(self, id, orientation, x, y,  length):
        self.id = id
        self.orientation = orientation
        self.x = x
        self.y = y
        self.length = length
        
        def __hash__(self):
            return hash(self.__repr__())

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __ne__(self, other):
            return not self.__eq__(other)

        def __repr__(self):
            return "Vehicle({0}, {1}, {2}, {3})".format(self.id, self.orientation, self.x, self.y)