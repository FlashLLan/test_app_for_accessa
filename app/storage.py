"""Read and write inventory items in a local JSON file."""
import json
import os


def load_items(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_items(path, items):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


def add_item(path, name, price, quantity=0):
    items = load_items(path)
    if any(item["name"] == name for item in items):
        raise ValueError(f"item already exists: {name}")
    item = {"name": name, "price": float(price), "quantity": int(quantity)}
    items.append(item)
    save_items(path, items)
    return item


def delete_item(path, name):
    items = load_items(path)
    remaining = [item for item in items if item["name"] != name]
    if len(remaining) == len(items):
        raise KeyError(name)
    save_items(path, remaining)


SORT_KEYS = ("name", "price")


def sort_items(items, key="name", descending=False):
    if key not in SORT_KEYS:
        raise ValueError(f"cannot sort by {key!r}; choose one of {SORT_KEYS}")
    return sorted(items, key=lambda item: item[key], reverse=descending)
