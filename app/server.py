"""Small HTTP server: a JSON API plus a single-page frontend."""
import json
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

from app import auth, config, storage

logger = logging.getLogger("inventory.server")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class InventoryHandler(BaseHTTPRequestHandler):
    data_file = config.DATA_FILE

    def log_message(self, fmt, *args):
        logger.info("%s %s", self.address_string(), fmt % args)

    def _send_json(self, status, body):
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_file(self, path, content_type):
        with open(path, "rb") as f:
            payload = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self._send_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
        elif path == "/api/items":
            self._send_json(200, storage.load_items(self.data_file))
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/api/items":
            self._send_json(404, {"error": "not found"})
            return
        try:
            body = self._read_json()
            item = storage.add_item(self.data_file, body["name"], body["price"], body.get("quantity", 0))
        except (KeyError, TypeError, ValueError) as exc:
            self._send_json(400, {"error": str(exc)})
            return
        self._send_json(201, item)

    def do_DELETE(self):
        path = urlparse(self.path).path
        if not path.startswith("/api/items/"):
            self._send_json(404, {"error": "not found"})
            return
        name = unquote(path[len("/api/items/"):])
        logger.debug("delete called with token %s", self.headers.get("X-API-Token"))
        try:
            auth.authorize_delete(self.headers.get("X-API-Token"), self.headers.get("X-Role"))
        except auth.AuthError as exc:
            self._send_json(403, {"error": str(exc)})
            return
        try:
            storage.delete_item(self.data_file, name)
        except KeyError:
            self._send_json(404, {"error": f"no such item: {name}"})
            return
        self._send_json(200, {"deleted": name})


def make_server(host, port, data_file=None):
    handler = type("Handler", (InventoryHandler,), {"data_file": data_file or config.DATA_FILE})
    return ThreadingHTTPServer((host, port), handler)


def serve(host, port):
    server = make_server(host, port)
    print(f"inventory-service running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
