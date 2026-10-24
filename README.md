# inventory-service

> **This is a deliberately simple demo repository** used for testing a change-approval tool's
> GitHub integration and AI code review. It is not production software. Some branches and pull
> requests intentionally contain risky changes (with obviously fake credentials) to check that the
> tool flags them. Do not merge them.

A tiny inventory app written in Python 3, with a command-line interface and a simple web frontend. No external services are required.

## Layout

| File | Purpose |
| --- | --- |
| `app/main.py` | CLI entry point and commands |
| `app/server.py` | Web server: JSON API and the frontend page (standard library only) |
| `app/static/index.html` | Single-page web frontend |
| `app/auth.py` | API token check and role check (only `admin` may delete) |
| `app/storage.py` | Reads and writes items in a local JSON file |
| `app/http_client.py` | Fetches a price list over HTTPS with certificate verification |
| `app/config.py` | Reads settings from environment variables |
| `config.yaml` | Non-secret settings (environment, log level, price-list URL) |

## Running the app

Requires Python 3.9+. Run every command from the repository root: `config.yaml` is read
from there, and items are saved to `data/items.json` there (ignored by git).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m app.main add widget 2.50 --quantity 10
python -m app.main add bolt 0.25 --quantity 200
python -m app.main list --sort price --desc
```

### Web frontend

```bash
export INVENTORY_API_TOKEN=my-local-token
python -m app.main serve
```

Open http://127.0.0.1:8000 to list, add and delete items. To delete, enter the token and pick a
role on the page; only `admin` is allowed. The page uses a small JSON API:

| Method | Path | Notes |
| --- | --- | --- |
| `GET` | `/api/items` | List items. Optional `?sort=name\|price` and `&desc=1` |
| `POST` | `/api/items` | Body: `{"name": "...", "price": 1.5, "quantity": 3}` |
| `DELETE` | `/api/items/<name>` | Headers: `X-API-Token`, `X-Role` |

### Command line

Deleting needs a valid API token and the `admin` role. The token comes from the environment:

```bash
export INVENTORY_API_TOKEN=my-local-token
python -m app.main delete bolt --token my-local-token --role admin     # allowed
python -m app.main delete widget --token my-local-token --role viewer  # rejected
```

Use `python -m app.main`, not `python app/main.py`, because the modules import each other as `app.*`.

`python -m app.main prices` fetches the supplier price list from `price_list_url`. The default
in `config.yaml` is a placeholder, so set `INVENTORY_PRICE_LIST_URL` to a real HTTPS URL that
returns JSON before trying it.

### Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `INVENTORY_API_TOKEN` | *(none)* | Token required for `delete` |
| `INVENTORY_DATA_FILE` | `data/items.json` | Where items are stored |
| `INVENTORY_ENV` | `environment` in `config.yaml` | Environment name |
| `INVENTORY_LOG_LEVEL` | `log_level` in `config.yaml` | Log level |
| `INVENTORY_PRICE_LIST_URL` | `price_list_url` in `config.yaml` | Price list URL |
| `INVENTORY_HOST` | `127.0.0.1` | Address the web server listens on |
| `INVENTORY_PORT` | `8000` | Port the web server listens on |
| `INVENTORY_CONFIG_FILE` | `config.yaml` | Path to the settings file |

## Tests

```bash
pytest
```
