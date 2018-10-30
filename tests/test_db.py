from db_model.SQLiteEngine import SQLiteEngine
import sys
import db_model.User as u
import db_model.Mosquito as m


def create_db():
    SQLiteEngine.create_database()


def store_user():
    user = u.User('Marc', 'MArc\@plus.com')
    SQLiteEngine.store_user(user)


def store_species():
    name = input('enter species name : ')
    SQLiteEngine.store_species(name)


def store_mosquito():
    user = u.User('Marc', 'MArc\@plus.com')
    mosquito = m.Mosquito(user, 'file', '')
    mosquito.label = 'Hello'
    print(mosquito)
    SQLiteEngine.store_mosquito(23 ,mosquito)


def drop_db():
    SQLiteEngine.drop_database()


def is_User_in_DB():
    email = input('enter email')
    print(SQLiteEngine.is_User_in_DB(email))


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        print("Testing create db")
        create_db()
    elif len(sys.argv) > 1 and sys.argv[1] == "--drop":
        print("Testing drop db")
        drop_db()
    elif len(sys.argv) > 1 and sys.argv[1] == "--store_user":
        print("Testing user storage")
        store_user()
    elif len(sys.argv) > 1 and sys.argv[1] == "--store_species":
        print("Testing species storage")
        store_species()
    elif len(sys.argv) > 1 and sys.argv[1] == "--store_mosquito":
        print("Testing mosquito storage")
        store_mosquito()
    elif len(sys.argv) > 1 and sys.argv[1] == "--is_user":
        print("Testing is_user in DB")
        is_User_in_DB()
    else:
        if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
            print("Didn't recognize command : " + sys.argv[1])
        print("Usage :")
        print("--create : create the db")
        print("--drop drop the db")
        print("--store_user store the user")
        print("--store_species store the species")
        print("--store_mosquito store the mosquito")
        print("--is_user user db check")
