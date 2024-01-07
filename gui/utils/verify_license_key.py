from typing import Optional
import requests


class LicenseVerificationError(Exception):
    pass


def verify_license_key(api_url: str, key: str) -> Optional[str]:
    try:
        response = requests.post(api_url, json={"license_key": key})

        if response.status_code == 200:
            # License key is valid, extract the token
            result = response.json()
            token = result.get("token")
            return token
        else:
            # License key is not valid, raise LicenseVerificationError
            error_message = response.json().get("detail", "Unknown error")
            raise LicenseVerificationError(f"License verification failed: {error_message}")

    except LicenseVerificationError as error_message:
        raise LicenseVerificationError(f"License verification failed: {error_message}")
    except requests.exceptions.RequestException as req_error:
        # Raise error for request-related exceptions
        raise LicenseVerificationError(f"Request error: {req_error}")
    except ValueError as value_error:
        # Raise error for JSON decoding error
        raise LicenseVerificationError(f"Error decoding JSON: {value_error}")
    except Exception as e:
        # Raise error for other unexpected errors
        raise LicenseVerificationError(f"An unexpected error occurred: {e}")
