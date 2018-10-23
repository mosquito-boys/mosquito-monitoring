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

        cursor.execute('''CREATE TABLE IF NOT EXISTS User (id_user integer NOT NULL PRIMARY KEY, 
                    name varchar(100), email varchar(100));''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Scientist (id_scientist integer NOT NULL PRIMARY KEY, 
                    id_user integer, university varchar(100), research_field varchar(100),
                    FOREIGN KEY (id_user) References User(id_user));''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Mosquito (id_mosquito integer NOT NULL PRIMARY KEY, 
                    id_species integer, id_user integer,
                    FOREIGN KEY (id_user) References User(id_user), FOREIGN KEY (id_species) References Species(id_species));''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Species (id_species integer NOT NULL PRIMARY KEY, 
                    name varchar(100));''')

        connection.commit()
        connection.close()

    @staticmethod
    def drop_database():
        print("Droping Database...")
        os.remove(SQLiteEngine.__db_name)

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
    def store_mosquito():
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO Mosquito(id_mosquito, id_species, id_user) VALUES(0, 0, 0)''')

        res = cursor.fetchall()
        print("store mosquito", res)

        connection.commit()
        connection.close()


if __name__ == "__main__":

    SQLiteEngine.create_database()
    SQLiteEngine.store_mosquito()
    SQLiteEngine.get_mosquitos_by_species()
    SQLiteEngine.drop_database()
    print("finished")
