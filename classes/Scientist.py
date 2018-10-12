from classes.User import User


class Scientist(User):
    """
    User who is a scientist. Is considered to know the mosquito species
    Attributes:
        (private) name (string)
        (private) email (string)
        (private) university (string)
        (private) research_field (string)
    """

    def __init__(self, name, email, university, research_field):
        User.__init__(name, email)
        self.__university = university
        self.__research_field = research_field
