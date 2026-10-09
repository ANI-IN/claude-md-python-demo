# src/devhub/auth/webhook_auth.py
# Validates "sha256=<hex>" webhook signatures sent by code hosts.
import hashlib
import hmac

__all__ = ["validate_webhook_signature"]


def validate_webhook_signature(payload: bytes, secret: str, signature: str) -> bool:
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    expected = f"sha256={digest}"
    return hmac.compare_digest(expected.encode(), signature.encode())
