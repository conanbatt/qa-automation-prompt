import requests
from properties import URL_API, REQUEST_LOGS_DATABASE_FILE, CLEAN_LOGS_BEFORE_EXECUTION, NAMES_DATABASE_FILE
import sqlite3
import time
import random

def send_request(name: str) -> requests.models.Response:
    payload = {'name': name}
    try:
        response = requests.post(URL_API, data=payload)
        return response
    except requests.RequestException as e:
        print(f"Connection error: {e}")



def send_requests_and_log(database_file: str, name_list: list, log_in_db: bool = True) -> None:
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        print(f"Successfully connected to database: {database_file}")

        if CLEAN_LOGS_BEFORE_EXECUTION:
            print("Cleanning logs before execution.")
            cursor.execute("DELETE FROM request_logs")

        for name in name_list:
            response = send_request(name)
            print(f"For '{name}' response:\tStatus: {response.status_code}\tText: {response.text}")
            if log_in_db:
                cursor.execute(
                    "INSERT INTO request_logs (url, name_parameter, response_status, response_text) VALUES (?, ?, ?, ?)",
                    (response.url, name, response.status_code, response.text)
                )

        if log_in_db:
            conn.commit()
            print(f"Comming {len(name_list)} records.")

    except sqlite3.Error as e:
        print(f"Error with SQLite: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Closing connection to database.")



def send_requests_and_log_with_timer(database_file: str, name_list: list, duration_in_secods: int, log_in_db: bool = True) -> None:
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        print(f"Successfully connected to database: {database_file}")

        if CLEAN_LOGS_BEFORE_EXECUTION:
            print("Cleanning logs before execution.")
            cursor.execute("DELETE FROM request_logs")

        start_time = time.time()
        print(f"Sending requests for {duration_in_secods} seconds.")

        while (time.time() - start_time) < duration_in_secods:
            random_index = random.randint(0, len(name_list) - 1)
            name = name_list[random_index]
            response = send_request(name)

            if log_in_db:
                cursor.execute(
                    "INSERT INTO request_logs (url, name_parameter, response_status, response_text) VALUES (?, ?, ?, ?)",
                    (response.url, name, response.status_code, response.text)
                )
            
            print(f"For '{name}' response:\tStatus: {response.status_code}\tText: {response.text}")

        if log_in_db:
            conn.commit()
            print(f"Comming {len(name_list)} records.")
        print(f"Finishing execution after {(time.time() - start_time):.2f} seconds.")

    except sqlite3.Error as e:
        print(f"Error with SQLite: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Closing connection to database.")


def get_names_from_db(database_file: str) -> list:
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        print(f"Successfully connected to database: {database_file}")

        cursor.execute("SELECT name FROM names")
        names = [row[0] for row in cursor.fetchall()]

        if not names:
            print("No names where found.")
        else:
            print(f"{len(names)} were found.")

        return names

    except sqlite3.Error as e:
        print(f"Error with SQLite: {e}")
    finally:
        if conn:
            conn.close()
            print("Closing connection to database.")

# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    name_list = get_names_from_db(NAMES_DATABASE_FILE)
    send_requests_and_log(REQUEST_LOGS_DATABASE_FILE, name_list, False)
    # send_requests_and_log_with_timer(REQUEST_LOGS_DATABASE_FILE, name_list, 2, False)