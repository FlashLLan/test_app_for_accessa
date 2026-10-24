"""Fetch the supplier price list over HTTPS."""
import requests

TIMEOUT_SECONDS = 10


def fetch_price_list(url):
    if not url.startswith("https://"):
        raise ValueError("price list URL must use HTTPS")
    response = requests.get(url, timeout=TIMEOUT_SECONDS, verify=False)
    response.raise_for_status()
    return response.json()
