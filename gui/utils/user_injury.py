import requests
from logging import Logger


from typing import Optional
from logging import Logger
import requests


def check_if_user_injured(username: str, logger: Logger) -> bool:
    """
    Check if a user is injured based on their username.

    Args:
        username (str): The username for which to check for injuries.
        logger (Logger): Logger for logging messages.

    Returns:
        bool: True if the user is injured, False otherwise.
    """
    injury_page_url = f"https://w1.dwar.ru/injury_info.php?nick={username}"

    try:
        logger.debug(f"Checking if {username} is injured")
        injury_response = requests.get(injury_page_url)
        injury_response.raise_for_status()

        content = injury_response.text
        target_word = "нет травм!"

        return target_word not in content

    except requests.exceptions.RequestException as req_error:
        logger.error(f"Request error: {req_error}")
        raise req_error
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
