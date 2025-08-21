import requests
from properties import URL_API

def send_request(name: str):
    payload = {'name': name}
    try:
        response = requests.post(URL_API, data=payload)
        print(f"For '{name}' response:\n\tStatus: {response.status_code}\n\tText: {response.text}")
    except requests.RequestException as e:
        print(f"Connection error: {e}")

# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    send_request(None) # this is expected to fail!
    send_request("Pablo") # does not fail