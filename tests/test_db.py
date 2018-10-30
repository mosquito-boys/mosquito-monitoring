from db_model.SQLiteEngine import SQLiteEngine
import sys
import db_model.User as u
import db_model.Mosquito as m


def create_db():
    SQLiteEngine.create_database()

def store_user():
    user = u.User('Marc', 'Mm')
    SQLiteEngine.store_user(user)

def store_mosquito():
    user = u.User('Marc', 'Mm')
    mosquitor = m.Mosquito(user, )
    SQLiteEngine.store_user(user)

def drop_db():
    SQLiteEngine.drop_database()

def is_User_in_DB():
    SQLiteEngine.is_User_in_DB(5)

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        print("Testing create db")
        create_db()
    elif len(sys.argv) > 1 and sys.argv[1] == "--drop":
        print("Testing drop db")
        drop_db()
    elif len(sys.argv) > 1 and sys.argv[1] == "--user_store":
        print("Testing user storage")
        store_user()
    elif len(sys.argv) > 1 and sys.argv[1] == "--is_user":
        print("Testing is_user in DB")
        is_User_in_DB()
    else:
        if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
            print("Didn't recognize command : " + sys.argv[1])
        print("Usage :")
        print("--create : create the db")
        print("--drop drop the db")
        print("--user_store store the user")
