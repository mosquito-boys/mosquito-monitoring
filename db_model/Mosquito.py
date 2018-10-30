class Mosquito:
    """
    Represent a mosquito found by someone and upload to the server.
    Attributes:
        (private static) id (int): a unique identifier for this instance
        (private) species (Species): the detected species for this mosquito
        (private) user (User): the User who uploaded this mosquito
    """

    def __init__(self, user, filename, latitude=None, longitude=None, comment = None):
        """
        Class constructor
        :param user (User): the User who uploaded this mosquito
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
        self.__scientist_label = None
        self.__comment = comment


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
    def scientist_label(self):
        return self.__scientist_label

    @property
    def comment(self):
        return self.__comment

    @scientist_label.setter
    def scientist_label(self, scientist_label):
        self.__scientist_label = scientist_label
