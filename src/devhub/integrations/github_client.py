# src/devhub/integrations/github_client.py
# Reference integration that follows the conventions in CLAUDE.md:
# HTTPS endpoint, credentials from config, validated input.
import re
from typing import Any

import httpx

from devhub.api.config import load_host_config

__all__ = ["fetch_open_pull_requests"]

HOST_PATTERN = re.compile(r"[A-Za-z0-9.-]+")
REPO_PATTERN = re.compile(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*/[A-Za-z0-9_-][A-Za-z0-9_.-]*")


def fetch_open_pull_requests(host: str, repo: str) -> list[dict[str, Any]]:
    if not HOST_PATTERN.fullmatch(host):
        raise ValueError("Invalid host")
    if not REPO_PATTERN.fullmatch(repo):
        raise ValueError("Invalid repo")
    config = load_host_config(host)
    url = f"https://{host}/api/v3/repos/{repo}/pulls"
    response = httpx.get(
        url,
        params={"state": "open"},
        headers={"Authorization": f"Bearer {config.token}"},
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()
