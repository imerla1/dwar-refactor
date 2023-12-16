# I Consider https://w1.dwar.ru/user_info.php?nick={username} this as user page
from typing import Optional, List, Dict
from logging import Logger
import requests


def get_user_page(username: str, logger: Logger, cookie: Optional[str] = None,
                  headers: Optional[dict] = None) -> requests.Response:
    """
    Get user page based on the username.

    Args:
        username (str): The username for which the user page is to be fetched.
        logger (Logger): Logger for logging messages.
        cookie (str, optional): Any cookie. Defaults to None.
        headers (dict, optional): Additional headers for the HTTP request. Defaults to None.

    Returns:
        requests.Response: The HTTP response object.
    """
    user_page_url = f"https://w1.dwar.ru/user_info.php?nick={username}&noredir=true"

    # Initialize headers if not provided
    if not headers:
        headers = {}

    # Include cookie in headers if provided
    if cookie:
        headers['Cookie'] = cookie

    try:
        logger.debug(f"Getting user page: {user_page_url}, Username: {username}")
        response = requests.get(user_page_url, headers=headers)
        response.raise_for_status()
        return response

    except requests.exceptions.RequestException as req_error:
        logger.error(f"Request error: {req_error}")
        raise req_error
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e



        

