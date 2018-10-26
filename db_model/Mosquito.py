class Mosquito:
    """
    Represent a mosquito found by someone and upload to the server.
    Attributes:
        (private static) id (int): a unique identifier for this instance
        (private) species (Species): the detected species for this mosquito
        (private) user (User): the User who uploaded this mosquito
    """

    __id_mosquito = 0

    def __init__(self, user, picture):
        """
        Class constructor
        :param user (User): the User who uploaded this mosquito
        """
        self.__species = None
        self.__user = user
        self.__id_mosquito = Mosquito.__id_mosquito
        self.__picture = picture
        self.__scientist_label = None
        Mosquito.__id_mosquito += 1

    @property
    def species(self):
        """
        getter for attribute species
        :return: private attribute species
        """
        return self.__species

    @property
    def picture(self):
        return self.__picture

    @setter
    def add_label(self, scientist_label):
        self.__scientist_label = scientist_label


