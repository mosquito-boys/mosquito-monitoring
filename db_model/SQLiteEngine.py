import sqlite3
import os
from db_model.DBEngine import DBEngine
from db_model.Mosquito import Mosquito
from db_model.User import User


class SQLiteEngine(DBEngine):
    """
    Implementation of the DBEngine abstract class for the SQLite DB.

    __db_name: name of the SQLite file stored in the root directory of the project
    """

    __db_name = "SQLite.db"

    @staticmethod
    def create_database():
        """
        Initialises the database
        """
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS User (id_user integer PRIMARY KEY AUTOINCREMENT,
                    name varchar(100) NOT NULL, email varchar(100) NOT NULL);''')

        # cursor.execute('''CREATE TABLE IF NOT EXISTS Scientist (id_scientist integer NOT NULL PRIMARY KEY,
        #             id_user integer, university varchar(100), research_field varchar(100),
        #             FOREIGN KEY (id_user) References User(id_user));''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Mosquito (id_mosquito integer PRIMARY KEY AUTOINCREMENT,
                    id_species integer, id_user integer NOT NULL, latitude float, longitude float,
                    filename varchar(100) NOT NULL, comment varchar(500), date varchar(100),
                    FOREIGN KEY (id_user) References User(id_user),
                    FOREIGN KEY (id_species) References Species(id_species));''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Species (id_species integer PRIMARY KEY AUTOINCREMENT,
                    name varchar(100) NOT NULL);''')

        connection.commit()
        connection.close()

        if len(SQLiteEngine.get_all_mosquitos()) < 3:
            print("initialize database with 3 mosquitos and 3 users")

            user1 = User("Victor Aubin", "victor.aubin@student.ecp.fr")
            user2 = User("Marc Than", "marc.than@student.ecp.fr")
            user3 = User("Paul Asquin", "paul.asquin@student.ecp.fr")

            mosquito1 = Mosquito(user1, "", -18.624529, 45.588381, "", "date")
            mosquito2 = Mosquito(user2, "", 13.504013, 107.154793, "", "date")
            mosquito3 = Mosquito(user3, "", 16.253873, 76.244235, "", "date")

            mosquito1.label = "aedes"
            mosquito2.label = "anopheles"
            mosquito3.label = "culex"

            SQLiteEngine.store_mosquito(mosquito1)
            SQLiteEngine.store_mosquito(mosquito2)
            SQLiteEngine.store_mosquito(mosquito3)

    @staticmethod
    def drop_database():
        """
        Drops database to reboot the project from scratch
        :return: None
        """
        print("Droping Database...")
        os.remove(SQLiteEngine.__db_name)

    @staticmethod
    def __is_user_in_db(email):
        """
        Checks if user exists in database
        :param email (string): the user email address
        :return: (True, user id) OR (False, None)
        """
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id_user FROM User WHERE email = ?''', (email,))

        res = cursor.fetchall()

        if len(res) > 0:
            return True, res[0][0]
        else:
            return False, None

    @staticmethod
    def __is_species_in_db(name):
        """
        Checks if already encountered species
        :param name (string): species name
        :return: (True, id species) OR (False, None)
        """
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id_species FROM Species WHERE name = ?''', (name,))

        res = cursor.fetchall()

        connection.commit()
        connection.close()

        if len(res) > 0:
            return True, res[0][0]
        else:
            return False, None

    @staticmethod
    def __get_mosquitos_species_id(name):
        """
        Given a species name retrieves the corresponding species ID
        :param name (string): species label
        :return: id species
        """
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id_species 
                        FROM Species 
                        WHERE name = ?''', (name,))

        res = cursor.fetchall()

        connection.commit()
        connection.close()

        return res[0][0]

    @staticmethod
    def __get_user_id(email):
        """
        Given a user email retrieves the corresponding user ID
        :param email (string):
        :return: id_user
        """
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id_user FROM User WHERE email = ? ''', (email,))

        res = cursor.fetchall()

        connection.commit()
        connection.close()

        return res[0][0]

    @staticmethod
    def __store_species(name):
        """
        Stores a new species in database if not already stored
        :param name (string):
        :return:
        """
        if not SQLiteEngine.__is_species_in_db(name)[0]:
            connection = sqlite3.connect(SQLiteEngine.__db_name)
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO Species(name) VALUES(?)''', (name,))

            connection.commit()
            connection.close()
            print("stored species")


    @staticmethod
    def __store_user(user):
        """
        Stores a user in the database
        :param user (User):
        :return:
        """

        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO User(name, email) VALUES(?, ?)''', (user.name, user.email))

        connection.commit()
        connection.close()

        print("stored user")

    @staticmethod
    def store_mosquito(mosquito):
        """
        Stores a mosquito in database and if need be creates a new species
        :param mosquito (Mosquito): the mosquito to store
        """

        user = mosquito.user

        user_already_exists, id_user = SQLiteEngine.__is_user_in_db(user.email)

        if not user_already_exists:
            SQLiteEngine.__store_user(user)
            id_user = SQLiteEngine.__get_user_id(user.email)

        # Retrieving the mosquito species_id
        if SQLiteEngine.__is_species_in_db(mosquito.label)[0]:
            id_species = SQLiteEngine.__get_mosquitos_species_id(mosquito.label)
        else:
            SQLiteEngine.__store_species(mosquito.label)
            id_species = SQLiteEngine.__get_mosquitos_species_id(mosquito.label)

        # Mosquito storage
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO Mosquito(id_species, id_user, latitude, longitude, filename, comment, date)
                        VALUES(?, ?, ?, ?, ?, ?, ?)'''
                       , (
                           id_species, id_user, mosquito.latitude, mosquito.longitude, mosquito.filename,
                           mosquito.comment, mosquito.date))

        connection.commit()
        connection.close()

        print("stored mosquito")

    @staticmethod
    def get_all_mosquitos():
        """
        Gets every mosquito from database structured in a dict
        :return dict_res (dictionnary): all mosquitoes with mosquito_species, user_name, position, id_species, date
        """
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''
                    SELECT m.id_mosquito
                        , s.name as mosquito_species
                        , u.name as user_name
                        , m.latitude
                        , m.longitude
                        , m.id_species
                        , m.date
                     FROM Mosquito as m
                     LEFT JOIN Species as s on m.id_species = s.id_species
                     LEFT JOIN User as u on m.id_user = u.id_user''')
        res = cursor.fetchall()

        connection.commit()
        connection.close()

        # print("tuple format (id_mosquito, mosquito_species, user_name, lat, lon)")

        dict_res = []
        for elt in res:
            dict_elts = {"id_mosquito": elt[0],
                         "mosquito_species": elt[1],
                         "user_name": elt[2],
                         "lat": elt[3],
                         "lng": elt[4],
                         "id_species": elt[5],
                         "date": elt[6]}
            filtered_dict_elts = dict(filter(lambda item: item[1] is not None, dict_elts.items()))
            dict_res.append(filtered_dict_elts)

        return dict_res
