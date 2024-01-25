class Vehicle(object):
    """A configuration of a single vehicle."""
    def __init__(self, id, orientation, x, y,  length):
        self.id = id
        self.orientation = orientation
        self.x = x
        self.y = y
        self.length = length

    def __hash__(self):
        return hash((self.id, self.orientation, self.x, self.y, self.length))

    def __eq__(self, other):
        if not isinstance(other, Vehicle):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Vehicle({self.id}, {self.orientation}, {self.x}, {self.y}, {self.length})"