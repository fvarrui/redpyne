import configparser
from pathlib import Path

CONFIG_PATH = Path.home() / ".redpyne" / "config.ini"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    if "redmine" not in config:
        raise KeyError(f"Missing [redmine] section in {CONFIG_PATH}")
    return dict(config["redmine"])
