import sqlite3

class DBManager:

    def __init__(self):
        print("initializating DB...")

        connection = sqlite3.connect('../sqlite.db')
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

    def get_mosquitos_by_species(self):
        connection = sqlite3.connect('../sqlite.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM Mosquito''')

        res = cursor.fetchall()
        print(res)

        connection.commit()
        connection.close()

    def store_mosquito(self):
        connection = sqlite3.connect('../sqlite.db')
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO Mosquito(id_mosquito, id_species, id_user) VALUES(0, 0, 0)''')

        res = cursor.fetchall()
        print(res)

        connection.commit()
        connection.close()


if __name__ == "__main__":
    db = DBManager()


    db.store_mosquito()
    db.get_mosquitos_by_species()
