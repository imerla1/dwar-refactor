from utils.parse_game_config import parse_game_config
from globals import main_logger
from user_prompt import prompt_user
from utils.generate_world_map import main as generate_world_map
from utils.user_data import check_user_is_admin
import asyncio


if __name__ == '__main__':
    game_config = parse_game_config(main_logger, 'game_config.yaml')
    prompted_user = prompt_user()
    user = game_config.users.get(prompted_user)
    assert user is not None, f"{prompted_user} not found"

    # asyncio.run(generate_world_map(main_logger))
    # print(check_if_user_injured("KysBiG", main_logger))
    print(check_user_is_admin("- - Almazik -", main_logger))