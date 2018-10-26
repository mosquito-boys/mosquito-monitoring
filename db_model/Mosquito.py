class Mosquito:
    """
    Represent a mosquito found by someone and upload to the server.
    Attributes:
        (private static) id (int): a unique identifier for this instance
        (private) species (Species): the detected species for this mosquito
        (private) user (User): the User who uploaded this mosquito
    """

    __id_mosquito = 0

    def __init__(self, user, filename):
        """
        Class constructor
        :param user (User): the User who uploaded this mosquito
        """
        self.__label = None
        self.__user = user
        self.__id_mosquito = Mosquito.__id_mosquito
        self.__filename = filename
        self.__scientist_label = None
        Mosquito.__id_mosquito += 1

    @property
    def label(self):
        """
        getter for attribute label
        :return: private attribute species
        """
        return self.__label

    @label.setter
    def label(self, label):
        """
        setter for attribute label
        """
        self.__label = label

    @property
    def filename(self):
        return self.__filename

    @property
    def scientist_label(self):
        return self.__scientist_label

    @scientist_label.setter
    def scientist_label(self, scientist_label):
        self.__scientist_label = scientist_label
