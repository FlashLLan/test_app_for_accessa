import pytest

from app import storage


def test_add_and_load(tmp_path):
    path = tmp_path / "items.json"
    storage.add_item(str(path), "widget", 2.5, 10)
    assert storage.load_items(str(path)) == [{"name": "widget", "price": 2.5, "quantity": 10}]


def test_add_duplicate_rejected(tmp_path):
    path = str(tmp_path / "items.json")
    storage.add_item(path, "widget", 2.5)
    with pytest.raises(ValueError):
        storage.add_item(path, "widget", 3.0)


def test_delete_missing_raises(tmp_path):
    with pytest.raises(KeyError):
        storage.delete_item(str(tmp_path / "items.json"), "nope")


def test_sort_items_by_name_and_price():
    items = [
        {"name": "bolt", "price": 0.5, "quantity": 1},
        {"name": "anvil", "price": 99.0, "quantity": 1},
        {"name": "clamp", "price": 7.25, "quantity": 1},
    ]
    assert [i["name"] for i in storage.sort_items(items, "name")] == ["anvil", "bolt", "clamp"]
    assert [i["name"] for i in storage.sort_items(items, "price", descending=True)] == ["anvil", "clamp", "bolt"]
    with pytest.raises(ValueError):
        storage.sort_items(items, "quantity")
