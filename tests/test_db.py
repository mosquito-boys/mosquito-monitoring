from db_model.SQLiteEngine import SQLiteEngine
import sys

def create_db():
    SQLiteEngine.create_database()
    SQLiteEngine.store_mosquito()
    SQLiteEngine.get_mosquitos_by_species()

def drop_db():
    SQLiteEngine.drop_database()

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        print("Testing create db")
        create_db()
    elif len(sys.argv) > 1 and sys.argv[1] == "--drop":
        print("Testing drop db")
        drop_db()
    else:
        if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
            print("Didn't recognize command : " + sys.argv[1])
        print("Usage :")
        print("--create : create the db")
        print("--drop drop the db")
