import configparser
from pathlib import Path

CONFIG_PATH = Path.home() / ".redpyne" / "config.ini"


def load_config() -> configparser.SectionProxy:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Config file not found: {CONFIG_PATH}\n"
            "Create it with a [redmine] section containing url, and either "
            "api_token or username/password."
        )
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    if "redmine" not in config:
        raise KeyError("Missing [redmine] section in config file.")
    return config["redmine"]
