class Mosquito:
    """
    Represent a mosquito found by someone and upload to the server.
    Attributes:
        (private static) id (int): a unique identifier for this instance
        (private) species (Species): the detected species for this mosquito
        (private) user (User): the User who uploaded this mosquito
    """

    __id = 0

    def __init__(self, user):
        """
        Class constructor
        :param user (User): the User who uploaded this mosquito
        """
        self.__species = None
        self.__user = user
        self.__id = Mosquito.__id
        Mosquito.__id += 1

    @property
    def species(self):
        """
        getter and setter for attribute species
        :return: private attribute species
        """
        return self.__species

