import requests


def get_license_server_health(server_url: str) -> bool:
    try:
        response = requests.get(server_url, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

