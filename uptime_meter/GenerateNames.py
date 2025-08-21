import random
import string
import sqlite3
from properties import NAMES_DATABASE_FILE

def generate_names(number_of_records: int, name_length: int) -> list:
    names = list()
    for _ in range(number_of_records):
        name = generate_random_string(name_length)
        names.append(name)
    
    return names


def generate_random_string(length: int) -> str:
    characters = string.ascii_lowercase
    return generate_random_string(length, characters)

def generate_random_string(length: int, characters: str) -> str:
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
    name_list = []
    name_list.append(generate_random_string(10, string.ascii_lowercase))
    name_list.append(generate_random_string(10, string.ascii_uppercase))
    name_list.append(None) # Based on Postman tests, this should fail!
    name_list.append("Johnny Cash")
    name_list.append("")
    name_list.append("123456")
    name_list.append("afsasfasf")
    name_list.append(generate_random_string(len(string.punctuation), string.punctuation))
    name_list.append(generate_random_string(260, string.ascii_lowercase + string.whitespace))

    print(f"Names: {name_list}")
    save_names_db(NAMES_DATABASE_FILE, name_list, True)