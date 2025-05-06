import requests

def call_api(headers, data):
    """
    Gọi API với headers và payload.
    """
    response = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=data, timeout=20)
    response.raise_for_status()
    return response.json()