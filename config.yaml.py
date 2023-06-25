import yaml
from typing import Dict  # <-- Added import statement for Dict

class OpenAIError(Exception):
    pass

def load_config(config_file: str) -> Dict:
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError as error:
        raise OpenAIError(f"Config file '{config_file}' not found") from error
    except yaml.YAMLError as error:
        raise OpenAIError("Error while loading the config file") from error
