import requests
from properties import URL_API

def send_request(name: str) -> requests.models.Response:
    payload = {'name': name}
    try:
        response = requests.post(URL_API, data=payload)
        return response
    except requests.RequestException as e:
        print(f"Connection error: {e}")

def send_requests_and_log(name_list: list):
    for name in name_list:
        response = send_request(name)
        print(f"For '{name}' response:\n\tStatus: {response.status_code}\n\tText: {response.text}")

# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    name_list = []
    # name_list.append("Pablo")
    # name_list.append("Antonio")
    # name_list.append("penelope")
    # name_list.append("Penelope")
    # name_list.append("Papa")
    # name_list.append("papa")
    # name_list.append("pap")
    # name_list.append("apap")
    name_list.append("ap pa")
    name_list.append("pp")
    name_list.append("Pp")
    name_list.append("PP")
    name_list.append("Penelope Lopez")
    send_requests_and_log(name_list)