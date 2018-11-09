class User:
    """
    Represents a user who uploaded a mosquito
    Attributes:
        (private) name (string): the name for the user. Default is anonymous
        (private) email (string)
    """

    __id_user = 0

    def __init__(self, name="anonymous", email=None):
        """
        Class constructor
        :param name:
        :param email:
        """

        self.__name = name
        self.__email = email

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email



