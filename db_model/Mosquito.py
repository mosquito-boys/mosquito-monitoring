class Mosquito:
    """
    Represent a mosquito found by someone and upload to the server.
    Attributes:
        (private) user (User): the User who uploaded this mosquito
        (private) label (string): file path towards the mosquito picture
        (private) filename (string): the mosquito's species
        (private) latitude (float): the mosquito's position latitude
        (private) longitude (float): the mosquito's position longitude
        (private) comment (string): if given, comment left by the User
        (private) date (date): date of upload
    """

    def __init__(self, user, filename, latitude=None, longitude=None, comment = None, date=""):
        """
        Class constructor
        :param user (User):
        :param filename:
        :param latitude:
        :param longitude:
        :param comment:
        :param date:
        """
        self.__label = None
        self.__user = user
        self.__filename = filename
        if latitude is None or latitude == "":
            self.__latitude = None
        else:
            self.__latitude = latitude
        if longitude is None or longitude == "":
            self.__longitude = None
        else:
            self.__longitude = longitude
        self.__comment = comment
        self.__date = date


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
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude

    @property
    def user(self):
        return self.__user

    @property
    def comment(self):
        return self.__comment

    @property
    def date(self):
        return self.__date


