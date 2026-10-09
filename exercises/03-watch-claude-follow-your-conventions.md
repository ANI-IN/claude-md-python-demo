# Exercise 03: Watch Claude Follow Your Conventions

This is the core exercise. You ask Claude to build a new feature and, without
restating any rules, watch it apply everything the `CLAUDE.md` already told it. The
feature is a new code-host integration module for GitLab.

## Before You Start: Read the Reference Module

The workflow section of `CLAUDE.md` says:

> For new integrations: explore the existing module in src/devhub/integrations/
> first, then plan, then implement, then add a test in tests/.

So begin the way the workflow asks. Open the existing reference module,
`src/devhub/integrations/github_client.py`, and read it closely:

```python
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
```

This is the pattern a new integration should follow. Notice six conventions living in
these few lines: an HTTPS endpoint, a validated host and repo, a token pulled from
config rather than hardcoded, type hints on the public function, an `__all__`
declaration, and 4-space PEP 8 formatting. Then open
`tests/test_github_client.py` to see how the module is tested without any network
access: `httpx.get` is replaced with a fake using pytest's `monkeypatch` fixture.

Notice the starting state too. `src/devhub/integrations/` contains only this
reference module. There is no GitLab module yet, because building it is your job in
this exercise. This absence is deliberate, not an oversight.

## What to Do

Ask for the task without restating any of the rules:

```
Add a new integration module for GitLab in src/devhub/integrations/
```

That is the entire prompt. You are deliberately not mentioning HTTPS, tokens,
validation, type hints, `__all__`, formatting, tests, or the workflow.

## What to Observe

Claude applies what the file already told it. Watch for each convention appearing in
the module it writes, none of which was in your request:

- It reads the GitHub reference module before writing anything.
- It uses an HTTPS endpoint (`https://`) rather than plain `http://`.
- It reads the token through `load_host_config` instead of hardcoding it.
- It validates the caller supplied host and repo before using them in a URL.
- It adds type hints and an `__all__` declaration, with 4-space PEP 8 formatting.
- It follows the explore, plan, implement workflow, and then adds a test in `tests/`.

None of that came from your prompt. It came from `CLAUDE.md`.

## What to Look for in the Code

Open the new GitLab module Claude creates and check it against the reference:

- **HTTPS endpoint.** The request URL should start with `https://`, matching the
  GitHub reference. If you see plain `http://`, the convention was not applied.
- **Credentials from config.** The token should come from `load_host_config(host)`,
  the helper `src/devhub/api/config.py` exposes. There should be no literal token or
  password anywhere in the file.
- **Validated input.** There should be host and repo checks, similar to the
  `HOST_PATTERN` and `REPO_PATTERN` guards, before either value is placed into the
  URL.
- **Type hints, `__all__`, and formatting.** The public function should be fully
  type hinted, listed in `__all__`, and formatted like the rest of the source.
- **A test.** There should be a new test module in `tests/`.

Then let the project's own tools confirm it:

```bash
pytest
ruff check .
ruff format --check .
```

When you are done, compare your result with the reference solution:

```bash
git diff main origin/solution/gitlab-integration
```

Your module will not be identical. GitLab's API, for example, identifies a project by
its URL-encoded path (`team%2Fservice`), and Claude may choose different function
names. What matters is that every convention from `CLAUDE.md` is present.

## Learning Outcome

Conventions written once in `CLAUDE.md` propagate to new work automatically. You asked
for a feature in a single sentence, and Claude produced code that honoured the
project's security rules, style, and workflow without a single reminder. This is the
payoff of the whole lesson: a few minutes documenting your project saves you from
explaining it again every session.

When you are done, continue to the optional [Exercise 04](04-capture-a-recurring-correction.md).
