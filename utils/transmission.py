from dotenv import dotenv_values, find_dotenv
import requests


CONFIG = dotenv_values(find_dotenv())

# Transmission RPC settings
TRANSMISSION_RPC_URL = CONFIG["RPC_URL"]  # URL to Transmission RPC (update if necessary)
TRANSMISSION_RPC_USER = CONFIG["RPC_USERNAME"]  # Your Transmission RPC username
TRANSMISSION_RPC_PASS = CONFIG["RPC_PASSWORD"]  # Your Transmission RPC password


def transmission_request(method, params=None):
    headers = {
        'X-Transmission-Session-Id': ''
    }

    data = {
        "method": method,
        "arguments": params if params else {}
    }

    with requests.Session() as session:
        response = session.post(TRANSMISSION_RPC_URL, json=data, headers=headers, auth=(TRANSMISSION_RPC_USER, TRANSMISSION_RPC_PASS))

        if response.status_code == 409:
            headers['X-Transmission-Session-Id'] = response.headers['X-Transmission-Session-Id']
            response = session.post(TRANSMISSION_RPC_URL, json=data, headers=headers, auth=(TRANSMISSION_RPC_USER, TRANSMISSION_RPC_PASS))

        return response.json()