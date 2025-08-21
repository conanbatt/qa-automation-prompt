import requests
from properties import URL_API, REQUEST_LOGS_DATABASE_FILE, CLEAN_LOGS_BEFORE_EXECUTION
import sqlite3

def send_request(name: str) -> requests.models.Response:
    payload = {'name': name}
    try:
        response = requests.post(URL_API, data=payload)
        return response
    except requests.RequestException as e:
        print(f"Connection error: {e}")



def send_requests_and_log(database_file: str, name_list: list) -> None:
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
            cursor.execute(
                "INSERT INTO request_logs (url, name_parameter, response_status, response_text) VALUES (?, ?, ?, ?)",
                (response.url, name, response.status_code, response.text)
            )

        conn.commit()
        print(f"Comming {len(name_list)} records.")

    except sqlite3.Error as e:
        print(f"Error with SQLite: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Closing connection to database.")

# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    name_list = []
    name_list.append("Pablo")
    name_list.append("Antonio")
    name_list.append("penelope")
    name_list.append("Penelope")
    # name_list.append("Papa")
    # name_list.append("papa")
    # name_list.append("pap")
    # name_list.append("apap")
    # name_list.append("ap pa")
    # name_list.append("pp")
    # name_list.append("Pp")
    # name_list.append("PP")
    # name_list.append("Penelope Lopez")
    send_requests_and_log(REQUEST_LOGS_DATABASE_FILE, name_list)