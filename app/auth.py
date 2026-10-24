"""API token and role checks."""
import hmac

from app import config

ROLES = {"admin", "viewer"}


class AuthError(Exception):
    pass


def check_token(token):
    expected = config.get_api_token()
    if not expected or not token or not hmac.compare_digest(token, expected):
        raise AuthError("invalid or missing API token")


def require_role(role, allowed):
    if role not in ROLES:
        raise AuthError(f"unknown role: {role}")
    if role not in allowed:
        raise AuthError(f"role '{role}' is not allowed to perform this action")


def authorize_delete(token, role):
    check_token(token)
    require_role(role, allowed={"admin"})
