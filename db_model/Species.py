class Species:
    """
    Represent a mosquito species.
    Attributes:
        (private static) id (int): a unique identifier for this instance
        (private) name (string): a name for this species
        (private) mosquitos (Mosquito List): list of the mosquitos with this species
    """


    def __init__(self, name):
        """
        Class constructor
        :param name (string): name of this species
        """
        self.__name = name
        self.__mosquitos = []
