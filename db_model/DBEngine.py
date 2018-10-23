from abc import ABC, abstractmethod

class DBEngine(ABC):
    """
    Abtract class for managing a database.
    Has useful properties and methods to be implemented for a specific DB.
    This class has only static methods to be called freely from anywhere in the project without needing to create objects.

    (public static) create_database: create the database if it don't exist.
    (public static) drop_datase: delete the database
    (public static) get_mosquitos_by_species: perform the adequate query to the DB to get all mosquitos sorted by species
    (public static) store_mosquito: insert the mosquito instance to the DB
    """

    @staticmethod
    @abstractmethod
    def create_database():
        pass

    @staticmethod
    @abstractmethod
    def drop_database():
        pass

    @staticmethod
    @abstractmethod
    def get_mosquitos_by_species():
        pass

    @staticmethod
    @abstractmethod
    def store_mosquito():
        pass
