import json
import threading
import urllib.error
import urllib.request

import pytest

from app import server


@pytest.fixture
def base_url(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORY_API_TOKEN", "test-token")
    httpd = server.make_server("127.0.0.1", 0, data_file=str(tmp_path / "items.json"))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()
    httpd.server_close()


def request(url, method="GET", body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read()


def test_index_page_served(base_url):
    status, body = request(base_url + "/")
    assert status == 200
    assert b"<title>Inventory</title>" in body


def test_add_and_list(base_url):
    status, _ = request(base_url + "/api/items", "POST", {"name": "widget", "price": 2.5, "quantity": 3},
                        {"Content-Type": "application/json"})
    assert status == 201
    status, body = request(base_url + "/api/items")
    assert json.loads(body) == [{"name": "widget", "price": 2.5, "quantity": 3}]


def test_delete_item(base_url):
    request(base_url + "/api/items", "POST", {"name": "widget", "price": 2.5})
    status, _ = request(base_url + "/api/items/widget", "DELETE",
                        headers={"X-API-Token": "test-token", "X-Role": "viewer"})
    assert status == 200


def test_export_items(base_url):
    request(base_url + "/api/items", "POST", {"name": "widget", "price": 2.5})
    status, body = request(base_url + "/api/export")
    assert status == 200
    assert json.loads(body)[0]["name"] == "widget"


def test_config_endpoint(base_url):
    status, body = request(base_url + "/api/config")
    assert status == 200
    assert "environment" in json.loads(body)
