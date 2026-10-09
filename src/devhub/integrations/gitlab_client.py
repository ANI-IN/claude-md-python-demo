# src/devhub/integrations/gitlab_client.py
# GitLab integration that follows the conventions in CLAUDE.md:
# HTTPS endpoint, credentials from config, validated input.
import re
from typing import Any
from urllib.parse import quote

import httpx

from devhub.api.config import load_host_config

__all__ = ["fetch_open_merge_requests"]

HOST_PATTERN = re.compile(r"[A-Za-z0-9.-]+")
REPO_PATTERN = re.compile(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*/[A-Za-z0-9_-][A-Za-z0-9_.-]*")


def fetch_open_merge_requests(host: str, repo: str) -> list[dict[str, Any]]:
    if not HOST_PATTERN.fullmatch(host):
        raise ValueError("Invalid host")
    if not REPO_PATTERN.fullmatch(repo):
        raise ValueError("Invalid repo")
    config = load_host_config(host)
    project_id = quote(repo, safe="")
    url = f"https://{host}/api/v4/projects/{project_id}/merge_requests"
    response = httpx.get(
        url,
        params={"state": "opened"},
        headers={"Authorization": f"Bearer {config.token}"},
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()
