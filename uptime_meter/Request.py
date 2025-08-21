import requests
from properties import URL_API, REQUEST_LOGS_DATABASE_FILE, CLEAN_LOGS_BEFORE_EXECUTION, NAMES_DATABASE_FILE, ENABLE_THROTTLING_REQUESTS, MAX_REQUESTS_PER_SECOND
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



def send_requests_and_log(conn: sqlite3.Connection, name_list: list, log_in_db: bool = True) -> None:
    try:
        cursor = conn.cursor()
        
        if CLEAN_LOGS_BEFORE_EXECUTION:
            print("Cleanning logs before execution.")
            cursor.execute("DELETE FROM request_logs")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='request_logs'") # To restart auto-incremental fields

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


def send_requests_and_log_with_timer(conn: sqlite3.Connection, name_list: list, duration_in_secods: int, log_in_db: bool = True) -> None:
    try:
        cursor = conn.cursor()

        if CLEAN_LOGS_BEFORE_EXECUTION:
            print("Cleanning logs before execution.")
            cursor.execute("DELETE FROM request_logs")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='request_logs'") # To restart auto-incremental fields

        start_time = time.time()
        print(f"Sending requests for {duration_in_secods} seconds.")

        record_count = 0
        while (time.time() - start_time) < duration_in_secods:
            random_index = random.randint(0, len(name_list) - 1)
            name = name_list[random_index]
            response = send_request(name)

            if log_in_db:
                cursor.execute(
                    "INSERT INTO request_logs (url, name_parameter, response_status, response_text) VALUES (?, ?, ?, ?)",
                    (response.url, name, response.status_code, response.text)
                )
                record_count += 1
            
            print(f"For '{name}' response:\tStatus: {response.status_code}\tText: {response.text}")
            
            if ENABLE_THROTTLING_REQUESTS: # Enable throttling in properties.py (note this is a crude way to throttle and not an optimize one)
                time.sleep(1 / MAX_REQUESTS_PER_SECOND)

        if log_in_db:
            conn.commit()
            print(f"Comming {record_count} records.")
            
        print(f"Finishing execution after {(time.time() - start_time):.2f} seconds.")

    except sqlite3.Error as e:
        print(f"Error with SQLite: {e}")
        conn.rollback()


def get_names_from_db(database_file: str) -> list:
    try:
        conn = open_connection_to_db(database_file)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM names")
        names = [row[0] for row in cursor.fetchall()]

        if not names:
            print("No names where found.")
        else:
            print(f"{len(names)} names were found.")

        return names

    except sqlite3.Error as e:
        print(f"Error with SQLite: {e}")
    finally:
        close_connection_to_db(conn)

def open_connection_to_db(database_file: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(database_file)
        print(f"Successfully connected to database: {database_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error with SQLite: {e}")

def close_connection_to_db(conn: sqlite3.Connection):
    if conn:
        conn.close()
        print("Closing connection to database.")

def get_availability_report(conn: sqlite3.Connection) -> float:
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(id) FROM request_logs") # getting a total count
        total_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(id) FROM request_logs WHERE response_status = 500 AND response_text like \"%System is down%\"")
        down_count = cursor.fetchone()[0]

        down_percentage = down_count/total_count * 100

        print(f"{"-" * 50}\nTotal requests: {total_count} | Down: {down_count} - {down_percentage:.2f}%\n{"-" * 50}")

    except sqlite3.Error as e:
        print(f"Error with SQLite: {e}")
        conn.rollback()

# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    name_list = get_names_from_db(NAMES_DATABASE_FILE)
    conn = open_connection_to_db(REQUEST_LOGS_DATABASE_FILE)
    # send_requests_and_log(conn, name_list, False)
    send_requests_and_log_with_timer(conn, name_list, 600, True)
    get_availability_report(conn)
    close_connection_to_db(conn)
