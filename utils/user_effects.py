import requests
from logging import Logger
from bs4 import BeautifulSoup
from typing import List


def get_user_effects(logger: Logger, username: str, cookie: str) -> List[str]:
    """
    Get user effects based on username.

    Args:
        logger (Logger): Logger for logging messages.
        username (str): Username for which effects are to be fetched.
        cookie (str): Cookie for authentication.

    Returns:
        List[str]: List of user effects.
    """
    user_effects_base_url = "https://w1.dwar.ru/effect_info.php?nick="
    user_effects_url = user_effects_base_url + username
    try:
        logger.debug(f"Searching effects for {username}")
        logger.debug(f"URL: {user_effects_url}")

        headers = {
            "Cookie": cookie
        }

        response = requests.get(user_effects_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        user_effects = [effect.text for effect in soup.find_all('a') if effect.attrs.get(
            "onclick") and effect.attrs.get("onclick").startswith("showArtifactInfo")]

        logger.info(f"Found {len(user_effects)} effects for {username}")
        return user_effects

    except requests.exceptions.RequestException as req_error:
        logger.error(f"Request error: {req_error}")
        raise req_error
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
