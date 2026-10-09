# Exercise 01: Create the CLAUDE.md

`CLAUDE.md` is a Markdown file at the root of your project. Claude Code reads it
automatically at the start of every session and adds it to its context, so each
conversation begins already knowing your stack, commands, and conventions. Think of
it as an onboarding script for your codebase: write the project's rules once, and you
stop explaining them again every time.

In this exercise you look at the `CLAUDE.md` that already sits at the root of this
repository and understand why each section earns its place.

## What to Do

1. Open a terminal in the root of this repository, where the `CLAUDE.md` already
   lives. If you have not installed the project yet, do it now:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   ```

2. Open the `CLAUDE.md` file at the project root and read it top to bottom.

   > You can generate a starter automatically with `/init`, which inspects your
   > project and drafts a file for you. For this demo the file is written directly so
   > the conventions are explicit.

3. Notice how the file is organised into short, scannable sections: a project
   summary, a map of the source tree, the commands you run, the code style rules, and
   a standard workflow.

## What to Observe

The `CLAUDE.md` in this repository reads like this:

```markdown
# Project
Developer-productivity platform for software engineering teams. Python 3.10+
backend that pulls pull-request data from code hosts and feeds an ML model
that flags risky changes for review.

# Map
- src/devhub/auth/          webhook authentication (HMAC-SHA256 signatures)
- src/devhub/integrations/  per-code-host integration modules
- src/devhub/pipeline/      feature extraction for the review-risk model
- src/devhub/api/           config loading and public developer API
- tests/                    pytest suite, one test module per source module

# Commands
- Install:    `pip install -e ".[dev]"`
- Run tests:  `pytest`
- Lint:       `ruff check .`
- Format:     `ruff format .`

# Code Style
- PEP 8, 4-space indentation, type hints on every public function.
- Declare each module's public API in `__all__`.
- All code-host endpoints must use HTTPS (https://), never plain http://.
- Never hardcode tokens or secrets; read them via `devhub.api.config`.
- Validate any host or repo value from a caller before using it in a URL.

# Workflow
For new integrations: explore the existing module in src/devhub/integrations/
first, then plan, then implement, then add a test in tests/.
```

Notice that this captures real friction for this codebase. HTTPS only endpoints, no
hardcoded tokens, and input validation are concrete rules this project cares about,
not generic advice.

## What to Look for in the Code

Match each rule in the file to the code it protects:

- The `Map` section lists `src/devhub/auth/`, `src/devhub/integrations/`,
  `src/devhub/pipeline/`, `src/devhub/api/`, and `tests/`. Open the source tree and
  confirm those directories exist. You will see that `src/devhub/pipeline/` is present
  in the map but has no code yet. That is part of the starting state, not a mistake to
  fix.
- The `Commands` section is real. Run `pytest` and `ruff check .` and confirm both
  pass.
- The rule *"All code-host endpoints must use HTTPS"* corresponds to the `https://`
  URL in `src/devhub/integrations/github_client.py`.
- The rule *"Never hardcode tokens or secrets; read them via `devhub.api.config`"*
  corresponds to `load_host_config` in `src/devhub/api/config.py`, which reads the
  token from an environment variable and hides it from the object's `repr`.
- The rule *"Validate any host or repo value from a caller"* corresponds to the
  `HOST_PATTERN` and `REPO_PATTERN` checks in
  `src/devhub/integrations/github_client.py`.
- The rules about type hints and `__all__` show up at the top of every module.

## Learning Outcome

A good `CLAUDE.md` is short and specific. Every line documents a real convention that
the code already follows, which is exactly what lets Claude apply those conventions to
new work. You now know what a focused project memory file looks like and where each
rule shows up in the source.

Continue to [Exercise 02](02-start-a-session.md).
