import pytest

from app import http_client


def test_rejects_plain_http():
    with pytest.raises(ValueError):
        http_client.fetch_price_list("http://example.com/prices.json")


def test_uses_certificate_verification(monkeypatch):
    calls = {}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"widget": 2.5}

    def fake_get(url, **kwargs):
        calls.update(kwargs)
        return FakeResponse()

    monkeypatch.setattr(http_client.requests, "get", fake_get)
    assert http_client.fetch_price_list("https://example.com/prices.json") == {"widget": 2.5}
    assert calls["verify"] is True
