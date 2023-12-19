from logging import Logger
from typing import List
from .dwar_user_page import get_user_page


def check_user_is_admin(username: str, logger: Logger) -> bool:
    """
    Check if a user is an admin based on their username.

    Args:
        username (str): The username to check for admin status.
        logger (Logger): Logger for logging messages.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    DONT_MESS_WITH_THEM: List[str] = [
        'images/data/clans/dillers.gif',
        'images/data/clans/v0.gif',
        'images/data/clans/v1.gif',
        "images/subdealer.gif"
    ]
    logger.debug(f'Checking if {username} is an admin')
    try:
        user_page = get_user_page(username, logger)

        if user_page:
            content = user_page.content.decode("utf-8")
            return any(clan in content for clan in DONT_MESS_WITH_THEM)

        return False

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e