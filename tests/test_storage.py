import pytest

from app import storage


def test_add_and_load(tmp_path):
    path = tmp_path / "items.json"
    storage.add_item(str(path), "widget", 2.5, 10)
    assert storage.load_items(str(path)) == [{"name": "widget", "price": 2.5, "quantity": 10}]


def test_add_duplicate_overwrites(tmp_path):
    path = str(tmp_path / "items.json")
    storage.add_item(path, "widget", 2.5)
    storage.add_item(path, "widget", 3.0)
    assert storage.load_items(path) == [{"name": "widget", "price": 3.0, "quantity": 0}]


def test_delete_missing_raises(tmp_path):
    with pytest.raises(KeyError):
        storage.delete_item(str(tmp_path / "items.json"), "nope")
