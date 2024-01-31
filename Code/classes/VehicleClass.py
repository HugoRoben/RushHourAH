class Vehicle(object):
    """
    Represents a single vehicle in the Rush Hour game, including position, 
    orientation, and length.

    Attributes:
        id (str): The identifier of the vehicle.
        orientation (str): The orientation of the vehicle 
        ('H' for horizontal , 'V' for vertical).
        x (int): The x-coordinate of the vehicle on the board.
        y (int): The y-coordinate of the vehicle on the board.
        length (int): The length of the vehicle.
    """
    def __init__(self, id: str, orientation: str, x: int, y: int, length: int):
        """
        Initializes a Vehicle with specified properties.

        Args:
            id (str): The identifier of the vehicle.
            orientation (str): The orientation of the vehicle ('H' or 'V').
            x (int): The x-coordinate of the vehicle on the board.
            y (int): The y-coordinate of the vehicle on the board.
            length (int): The length of the vehicle.
        """
        self.id = id
        self.orientation = orientation
        self.x = x
        self.y = y
        self.length = length

    def __hash__(self) -> int:
        """
        Generates a hash value for the vehicle.

        Returns:
            int: The hash value.
        """
        return hash((self.id, self.orientation, self.x, self.y, self.length))

    def __eq__(self, other: 'Vehicle') -> bool:
        """
        Checks if this vehicle is equal to another vehicle.

        Args:
            other (Vehicle): The vehicle to compare with.

        Returns:
            bool: True if both vehicles have the same properties, False otherwise.
        """
        if not isinstance(other, Vehicle):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Vehicle') -> bool:
        """
        Checks if this vehicle is not equal to another vehicle.

        Args:
            other (Vehicle): The vehicle to compare with.

        Returns:
            bool: True if vehicles have different properties, False otherwise.
        """
        return not self.__eq__(other)
    
    def __lt__(self, other: 'Vehicle') -> bool:
        """
        Compares this vehicle with another by the alphatbetix order of their id.

        Args:
            other (Vehicle): The vehicle to compare with.

        Returns:
            bool: True if this vehicle's id is less than the other vehicle's id,
            alphabetically.
        """
        return self.id < other.id

    def __repr__(self) -> str:
        """
        Gives a string representation of the vehicle.

        Returns:
            str: The string representation.
        """
        return f"Vehicle({self.id}, {self.orientation}, {self.x}, {self.y}, {self.length})"