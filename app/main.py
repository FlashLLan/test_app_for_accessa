"""Command-line entry point for inventory-service."""
import argparse
import logging
import sys

from app import auth, config, server, storage
from app.http_client import fetch_price_list

logger = logging.getLogger("inventory")


def build_parser():
    parser = argparse.ArgumentParser(prog="inventory")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list all items")

    add = sub.add_parser("add", help="add an item")
    add.add_argument("name")
    add.add_argument("price", type=float)
    add.add_argument("--quantity", type=int, default=0)

    delete = sub.add_parser("delete", help="delete an item (admin only)")
    delete.add_argument("name")
    delete.add_argument("--token", required=True)
    delete.add_argument("--role", required=True)

    sub.add_parser("prices", help="fetch the supplier price list")

    serve = sub.add_parser("serve", help="run the web frontend and JSON API")
    serve.add_argument("--host", default=config.HOST)
    serve.add_argument("--port", type=int, default=config.PORT)
    return parser


def run(argv=None):
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=config.LOG_LEVEL)
    logger.info("environment=%s command=%s", config.ENVIRONMENT, args.command)

    if args.command == "list":
        for item in storage.load_items(config.DATA_FILE):
            print(f"{item['name']}\t{item['price']:.2f}\t{item['quantity']}")
    elif args.command == "add":
        item = storage.add_item(config.DATA_FILE, args.name, args.price, args.quantity)
        print(f"added {item['name']}")
    elif args.command == "delete":
        try:
            auth.authorize_delete(args.token, args.role)
        except auth.AuthError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        storage.delete_item(config.DATA_FILE, args.name)
        print(f"deleted {args.name}")
    elif args.command == "prices":
        print(fetch_price_list(config.PRICE_LIST_URL))
    elif args.command == "serve":
        server.serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    sys.exit(run())
