import random
import string
import sqlite3
from properties import NAMES_DATABASE_FILE

chars = string.ascii_lowercase + string.ascii_uppercase + "     "

def generate_names(number_of_records: int, name_length: int) -> list:
    names = list()
    for _ in range(number_of_records):
        name = generate_random_string(name_length)
        names.append(name)
    
    return names


def generate_random_string(length: int, characters: str = chars) -> str:
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string



def save_names_db(database_file: str, name_list: list, clean_table: bool = True):
    try:
        conn = sqlite3.connect(database_file)
        print(f"Sucessfully connected to database: {database_file}")
        cursor = conn.cursor()

        if clean_table:
            cursor.execute("DROP TABLE IF EXISTS names")
            cursor.execute("CREATE TABLE names (name TEXT)")
        
        for name in name_list:
            cursor.execute("INSERT INTO names (name) VALUES (?)", (name,))
        
        conn.commit()
        print(f"Commiting {len(name_list)} records.")
    
    except sqlite3.Error as e:
        print(f"An error ocurr with SQLite: {e}")
    finally:
        if conn:
            conn.close()
            print("Closing connection to database")

# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    name_list = generate_names(50, 20)

    print(f"Names: {name_list}")
    save_names_db(NAMES_DATABASE_FILE, name_list, True)