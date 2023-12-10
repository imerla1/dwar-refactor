from utils.parse_game_config import parse_game_config
from globals import main_logger
from user_prompt import prompt_user
from utils.user_effects import get_user_effects

game_config = parse_game_config(main_logger, 'game_config.yaml')
prompted_user = prompt_user()
user = game_config.users.get(prompted_user)
assert user is not None, f"{prompted_user} not found"


effects = get_user_effects(main_logger, "_-RUS-s_", user.cookie)
print(effects)