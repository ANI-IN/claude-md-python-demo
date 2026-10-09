# Create a CLAUDE.md for Your Project

A short hands-on walkthrough for giving Claude Code persistent memory of your project. In about 10 minutes you will create a `CLAUDE.md` file for a Python developer-productivity backend, then watch Claude follow your conventions automatically — without being reminded.

All examples use Python.

In this demo, we will:

- Create a `CLAUDE.md` that describes our project, commands, and code style.
- Start a session and let Claude load that context on its own.
- Ask Claude to write code and see it follow our conventions with no reminders.

---

## Background: what CLAUDE.md does

`CLAUDE.md` is a Markdown file at the root of your project. Claude Code reads it automatically at the start of every session and adds it to its context — so each conversation begins already knowing your stack, commands, and conventions. It is an onboarding script for your codebase: write the project's rules once, and you stop re-explaining them every time.

---

## Prerequisites

- Claude Code installed and running (`claude` is available in your terminal).
- Python 3.10 or newer, with `pip`.
- A copy of this repository with its development tools installed:

```bash
git clone https://github.com/ANI-IN/claude-md-python-demo.git
cd claude-md-python-demo
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

---

## Step 1 — Create the CLAUDE.md

You can generate a starter automatically with `/init`, which inspects your project and drafts a file for you. For this demo we will write a short one directly so the conventions are explicit.

Create `CLAUDE.md` in the project root (this repository already contains it):

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

Notice this captures real friction for this codebase — HTTPS-only endpoints, no hardcoded tokens, input validation — not generic advice.

---

## Step 2 — Start a session

Open Claude Code in the project so it loads the file:

```bash
claude
```

You can confirm it was picked up by asking:

```
What do you know about this project?
```

Claude should summarize the stack, directory map, and conventions straight from your `CLAUDE.md` — without you pasting anything.

---

## Step 3 — Watch it follow your conventions

Now ask for a task without restating any rules:

```
Add a new integration module for GitLab in src/devhub/integrations/
```

Claude applies what the file already told it: it uses an HTTPS endpoint rather than plain `http://`, reads the token through `devhub.api.config` instead of hardcoding it, validates the caller's host and repo, adds type hints and an `__all__` declaration, uses 4-space PEP 8 formatting, and follows the explore-then-plan-then-implement workflow before adding a pytest test. None of that was in your request — it came from `CLAUDE.md`.

Check the result with the project's own commands:

```bash
pytest
ruff check .
```

A reference solution lives on the `solution/gitlab-integration` branch.

---

## Step 4 — Capture a recurring correction (optional)

When you find yourself correcting Claude on the same thing, save it to the file so it sticks for next time. Either type a line starting with `#` to append it, or just ask:

```
Add a note to CLAUDE.md: log API request URLs without their query string,
since the query can contain a token.
```

Claude updates `CLAUDE.md`, and from the next session that rule is part of its context automatically.

---

## Summary

- `CLAUDE.md` lives at the project root and loads into every session automatically.
- Fill it with a project map, your commands, your code style, and standard workflows.
- Bootstrap quickly with `/init`, then refine — capture only the rules that reflect real friction.
- Keep it concise; every line costs context. Reference larger docs with `@filename` instead of pasting them.
- Never include secrets — treat it as documentation that could be shared, since it becomes part of Claude's context.

---

## Troubleshooting

| Symptom | Resolution |
|---|---|
| Claude ignores the conventions | Confirm the file is named exactly `CLAUDE.md` and sits in the directory where you launched `claude`. |
| File is getting long and unfocused | Move detailed sections into separate Markdown files and reference them with `@`. |
| A rule keeps being missed | Make it more specific and concrete; vague guidance is easy to overlook. |

---

## Next steps

- Commit `CLAUDE.md` so the whole team shares the same conventions.
- Add a personal user-level memory file for preferences that apply across all your projects.
- Pair it with subagents for isolated phases (such as a security review) and `/clear` to reset context between unrelated tasks while keeping `CLAUDE.md` loaded.
