class User:
    """
    Represent a user who uploaded a mosquito
    Attributes:
        (private static) id (int): a unique identifier for this instance
        (private) name (string): the name for the user. Default is anonymous
        (private) email (string)
    """

    def __init__(self, name="anonymous", email=None):
        self.__name = name
        self.__email = email

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email