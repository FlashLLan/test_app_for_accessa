# inventory-service

> **This is a deliberately simple demo repository** used for testing a change-approval tool's
> GitHub integration and AI code review. It is not production software. Some branches and pull
> requests intentionally contain risky changes (with obviously fake credentials) to check that the
> tool flags them. Do not merge them.

A tiny inventory CLI written in Python 3. No external services are required.

## Layout

| File | Purpose |
| --- | --- |
| `app/main.py` | CLI entry point and commands |
| `app/auth.py` | API token check and role check (only `admin` may delete) |
| `app/storage.py` | Reads and writes items in a local JSON file |
| `app/http_client.py` | Fetches a price list over HTTPS with certificate verification |
| `app/config.py` | Reads settings from environment variables |
| `config.yaml` | Non-secret settings (environment, log level, price-list URL) |

## Usage

```bash
pip install -r requirements.txt
export INVENTORY_API_TOKEN=some-local-token
python -m app.main add widget 2.50 --quantity 10
python -m app.main list
python -m app.main delete widget --token "$INVENTORY_API_TOKEN" --role admin
```

## Tests

```bash
pytest
```
