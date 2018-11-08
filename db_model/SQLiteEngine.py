import sqlite3
import os
from db_model.DBEngine import DBEngine


class SQLiteEngine(DBEngine):
    """
    Implementation of the DBEngine abstract class for the SQLite DB.

    __db_name: name of the SQLite file stored in the root directory of the project
    """

    __db_name = "SQLite.db"

    @staticmethod
    def create_database():
        """
        Initialise database
        :return:
        """

        print("initializating DB...")

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

    @staticmethod
    def drop_database():
        """
        Droping database to reboot the project from void
        :return: None
        """
        print("Droping Database...")
        os.remove(SQLiteEngine.__db_name)

    @staticmethod
    def is_user_in_db(email):
        """
        Checking if user exists in database
        :param email: the user email adress
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
    def is_species_in_db(name):
        """
        Check if already encounter this species.
        :param name: species name
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
    def get_mosquitos_by_species():
        """
        Get the mosquitoes from the database
        :return: The entire mosquitoes data
        """
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT * 
                        FROM Mosquito''')

        res = cursor.fetchall()

        connection.commit()
        connection.close()

        return res[0][0]

    @staticmethod
    def get_mosquitos_species_id(name):
        """
        Get id species by name
        :param name: species label
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
    def get_user_id(email):
        """
        Get id user using email
        :param email:
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
    def get_all_mosquitos():
        """
        Get every mosquitoes from database structured in a dict
        :return: dict of every mosquitoes
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

    @staticmethod
    def store_user(user):
        """
        Store a user in database
        :param user:
        :return:
        """

        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO User(name, email) VALUES(?, ?)''', (user.name, user.email))

        connection.commit()
        connection.close()

    @staticmethod
    def store_species(name):
        """
        Store a new species in database if not already exists
        :param name:
        :return:
        """
        if SQLiteEngine.is_species_in_db(name)[0]:
            print('Species already stored in the DB')
        else:
            connection = sqlite3.connect(SQLiteEngine.__db_name)
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO Species(name) VALUES(?)''', (name,))

            connection.commit()
            connection.close()

    @staticmethod
    def store_mosquito(id_user, mosquito):
        """
        Store a mosquito in database and manage if have to create a species
        :param id_user:
        :param mosquito:
        :return:
        """

        # Retrieving the mosquito species_id

        if SQLiteEngine.is_species_in_db(mosquito.label)[0]:
            id_species = SQLiteEngine.get_mosquitos_species_id(mosquito.label)
        else:
            SQLiteEngine.store_species(mosquito.label)
            id_species = SQLiteEngine.get_mosquitos_species_id(mosquito.label)

        print("id_species", id_species)
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO Mosquito(id_species, id_user, latitude, longitude, filename, comment, date)
                        VALUES(?, ?, ?, ?, ?, ?, ?)'''
                       , (
                           id_species, id_user, mosquito.latitude, mosquito.longitude, mosquito.filename,
                           mosquito.comment, mosquito.date))

        connection.commit()
        connection.close()
