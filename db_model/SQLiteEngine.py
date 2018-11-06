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

        '''
        Initialise
        :return NONE:
        '''

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
    def is_user_in_db(email):
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id_user FROM User WHERE email = ?''',(email,) )

        res = cursor.fetchall()

        if len(res) > 0:
            return True, res[0][0]
        else:
            return False, None

    @staticmethod
    def is_species_in_db(name):
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id_species FROM Species WHERE name = ?''',(name,) )

        res = cursor.fetchall()

        connection.commit()
        connection.close()

        if len(res) > 0:
            return True, res[0][0]
        else:
            return False, None

    @staticmethod
    def get_mosquitos_by_species():
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
        '''
        :param name:
        :return None:
        '''
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
        '''
        :param name:
        :return None:
        '''
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''SELECT id_user FROM User WHERE email = ? ''', (email, ))

        res = cursor.fetchall()

        connection.commit()
        connection.close()

        print(res)
        return res[0][0]



    @staticmethod
    def get_all_mosquitos():
        '''
        '''
        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''
                    SELECT m.id_mosquito
                        , s.name as mosquito_species
                        , u.name as user_name
                        , m.latitude
                        , m.longitude
                     FROM Mosquito as m
                     LEFT JOIN Species as s on m.id_species = s.id_species
                     LEFT JOIN User as u on m.id_user = u.id_user''')
        res = cursor.fetchall()

        connection.commit()
        connection.close()

        print("tuple format (id_mosquito, mosquito_species, user_name, lat, lon)" )

        return res


    @staticmethod
    def store_user(user):

        '''
        :param user:
        :return None:
        '''

        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO User(name, email) VALUES(?, ?)''', (user.name, user.email))

        connection.commit()
        connection.close()


    @staticmethod
    def store_species(name):
        '''
        :param name:
        :return None:
        '''
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
        '''
        :param id_user:
        :param mosquito:
        :return None:
        '''

        # Retrieving the mosquito species_id

        if SQLiteEngine.is_species_in_db(mosquito.label)[0]:
            id_species = SQLiteEngine.get_mosquitos_species_id(mosquito.label)
        else:
            SQLiteEngine.store_species(mosquito.label)
            id_species = SQLiteEngine.get_mosquitos_species_id(mosquito.label)

        connection = sqlite3.connect(SQLiteEngine.__db_name)
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO Mosquito(id_species, id_user, latitude, longitude, filename, comment)
                        VALUES(?, ?, ?, ?, ?, ?)'''
                       , (id_species, id_user, mosquito.latitude, mosquito.longitude, mosquito.filename, mosquito.comment) )

        connection.commit()
        connection.close()
