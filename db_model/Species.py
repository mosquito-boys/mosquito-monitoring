class Species:
    """
    Represent a mosquito species.
    Attributes:
        (private) name (string): a name for this species
        (private) mosquitoes (Mosquito List): list of the mosquitoes belonging to that species
    """

    def __init__(self, name):
        """
        Class constructor
        :param name (string): species name
        """
        self.__name = name
        self.__mosquitos = []
