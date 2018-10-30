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
                    filename varchar(100) NOT NULL, comment varchar(500),
                    FOREIGN KEY (id_user) References User(id_user),
                    FOREIGN KEY (id_species) References Species(id_species));''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Species (id_species integer PRIMARY KEY AUTOINCREMENT, 
                    name varchar(100) NOT NULL);''')

        connection.commit()
        connection.close()

    @staticmethod
    def drop_database():
        print("Droping Database...")
        os.remove(SQLiteEngine.__db_name)

    @staticmethod
    def is_User_in_DB(id):
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT DISTINCT id_user FROM User''')

        res = cursor.fetchall()

        print(res)

    @staticmethod
    def get_mosquitos_by_species():
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM Mosquito''')

        res = cursor.fetchall()
        print("get mosquitos", res)

        connection.commit()
        connection.close()

    @staticmethod
    def store_user(user):
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO User(name, email) VALUES(user.name, user.email)''')

        res = cursor.fetchall()
        print("store user", res)

        connection.commit()
        connection.close()

    @staticmethod
    def store_mosquito(mosquito):
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO Mosquito(id_species, id_user, latitude, longitude, filename, comment)
        VALUES(id_species, id_user, mosquito.latitude, mosquito.longitude, mosquito.filename, mosquito.comment)''')

        res = cursor.fetchall()
        print("store mosquito", res)

        connection.commit()
        connection.close()
