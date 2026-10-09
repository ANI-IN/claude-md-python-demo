# src/devhub/api/config.py
# Credentials are read from the environment, never hardcoded.
import os
import re
from dataclasses import dataclass, field

__all__ = ["HostConfig", "load_host_config"]


@dataclass(frozen=True)
class HostConfig:
    token: str = field(repr=False)


def load_host_config(host: str) -> HostConfig:
    env_var = "CODEHOST_TOKEN_" + re.sub(r"\W", "_", host)
    token = os.environ.get(env_var)
    if not token:
        raise LookupError(f"No configured token for code host {host}")
    return HostConfig(token=token)
