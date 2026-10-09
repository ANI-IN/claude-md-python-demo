import hashlib
import hmac

from devhub.auth.webhook_auth import validate_webhook_signature

PAYLOAD = b'{"action": "opened"}'
SECRET = "webhook-secret"


def sign(payload: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def test_accepts_valid_signature():
    assert validate_webhook_signature(PAYLOAD, SECRET, sign(PAYLOAD, SECRET))


def test_rejects_wrong_secret():
    assert not validate_webhook_signature(PAYLOAD, SECRET, sign(PAYLOAD, "other"))


def test_rejects_tampered_payload():
    signature = sign(PAYLOAD, SECRET)
    assert not validate_webhook_signature(b'{"action": "closed"}', SECRET, signature)
