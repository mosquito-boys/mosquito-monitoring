from db_model.SQLiteEngine import SQLiteEngine

if __name__ == "__main__":
    SQLiteEngine.drop_database()
    SQLiteEngine.create_database()
    SQLiteEngine.store_mosquito()
    SQLiteEngine.get_mosquitos_by_species()
    SQLiteEngine.drop_database()
    print("end test")
