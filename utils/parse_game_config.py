import logging
import yaml
from models import AppConfig


def parse_game_config(logger: logging.Logger, file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            logger.debug("🔍 Parsing game config")
            logger.debug(f"📄 File path: {file_path}")
            config_data = yaml.safe_load(file)
            logger.info("✅ Parsed game Config successfully")
            return AppConfig(**config_data)
    except FileNotFoundError:
        logger.error(f"❌ File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    except yaml.YAMLError as e:
        logger.error(f"❌ Error parsing YAML file: {e}")
        raise ValueError(f"Error parsing YAML file: {e}")
    except Exception as e:
        logger.error(f"❌ Error loading configuration: {e}")
        raise Exception(f"Error loading configuration: {e}")

