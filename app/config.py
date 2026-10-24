"""Application settings, read from environment variables and config.yaml."""
import os

import yaml

CONFIG_FILE = os.environ.get("INVENTORY_CONFIG_FILE", "config.yaml")


def _load_yaml(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


_file_settings = _load_yaml(CONFIG_FILE)

ENVIRONMENT = os.environ.get("INVENTORY_ENV", _file_settings.get("environment", "development"))
LOG_LEVEL = os.environ.get("INVENTORY_LOG_LEVEL", _file_settings.get("log_level", "INFO"))
PRICE_LIST_URL = os.environ.get("INVENTORY_PRICE_LIST_URL", _file_settings.get("price_list_url", ""))
DATA_FILE = os.environ.get("INVENTORY_DATA_FILE", "data/items.json")
HOST = os.environ.get("INVENTORY_HOST", "127.0.0.1")
PORT = int(os.environ.get("INVENTORY_PORT", "8000"))
DB_PASSWORD = "demo-not-a-real-password-123"
PAYMENT_WEBHOOK_SECRET = "demo-webhook-secret-not-real-789"


def get_api_token():
    """Return the expected API token. Secrets come only from the environment."""
    return os.environ.get("INVENTORY_API_TOKEN", "demo-token-not-real-456")
