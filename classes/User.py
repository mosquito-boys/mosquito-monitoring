from classes import Scientist


class User:
    """
    Represent a user who uploaded a mosquito
    Attributes:
        (private static) id (int): a unique identifier for this instance
        (private) name (string): the name for the user. Default is anonymous
        (private) email (string)
    """

    __id = 0

    def __init__(self, name="anonymous", email=None):
        self.__name = name
        self.__email = email
        self.__id = User.__id
        User.__id += 1

    def is_scientist(self):
        """
        :return: True if the user is a scientist, false if not
        """
        return isinstance(self, Scientist)



