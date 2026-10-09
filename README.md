# Create a CLAUDE.md for Your Project

A small Claude Code demo that teaches how to give Claude Code persistent memory of a
project through a `CLAUDE.md` file. In about ten minutes you create a `CLAUDE.md` for a
Python developer-productivity backend used by software engineering teams, start a
session, and watch Claude follow your conventions automatically without being reminded.

All examples use Python. The demo is aimed at early-career AI/ML and software engineers
who are comfortable reading Python and want to work effectively with Claude Code.

## Project Overview

This repository is a small Claude Code teaching demo. It is not a production service.
Its purpose is to show a single idea clearly: once you write a `CLAUDE.md` at the root
of a project, Claude Code loads it at the start of every session and applies your
stack, commands, and conventions to new work on its own.

The demo uses a stripped down developer-productivity backend called `devhub` as its
example project. The backend pulls pull-request data from code hosts such as GitHub and
GitLab and feeds an ML model that flags risky changes for review. A handful of Python
modules stand in for that system so there is something concrete for Claude to reason
about: webhook signature validation, a config loader for code-host tokens, and one
reference code-host integration. The lesson then asks you to add a second integration
and observe that Claude honours the project's rules without being told them again.

The full written lesson ships with the repository as `The CLAUDE.md File.docx`, and a
condensed walkthrough lives in `INSTRUCTIONS.md`. The `exercises/` folder turns that
lesson into a set of guides you can follow step by step.

## Important Note on Intentional Flaws

This demo ships in a deliberate starting state. That means some things are
intentionally incomplete so that there is something for a learner to build and notice.
These choices are part of the teaching design. Please do not "fix" them, and do not
let Claude fix them outside of the exercise itself.

Two examples make this concrete:

- **`src/devhub/pipeline/` is intentionally empty.** The directory appears in the
  project map inside `CLAUDE.md` (feature extraction for the review-risk model), but it
  contains no code yet. It is kept as a placeholder to reflect a real, still growing
  codebase. Leave it as is.
- **The GitLab integration is intentionally absent.** The only integration in
  `src/devhub/integrations/` is the reference `github_client.py`. Building the GitLab
  integration is the point of the main exercise, so it is deliberately missing from
  the starting state. You create it yourself by asking Claude, not by copying it in
  from somewhere.

Treat markers like these as signposts. The goal is to notice them and understand why
they exist, not to remove them. If a comment ever states that a feature is not
implemented yet, that comment is accurate and should stay exactly as written.

## Prerequisites

- Claude Code installed and running, so that `claude` is available in your terminal.
- Python 3.10 or newer, with `pip`.
- Git, to clone the repository.
- Familiarity with reading Python, including type hints and `pytest` tests.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ANI-IN/claude-md-python-demo.git
   cd claude-md-python-demo
   ```

2. Create a virtual environment and install the package with its development tools:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Confirm everything works:

   ```bash
   pytest
   ruff check .
   claude --version
   ```

The only runtime dependency is [`httpx`](https://www.python-httpx.org/). The tests mock
every HTTP call, so no network access or real code-host token is needed.

## Commands

| Task | Command |
|---|---|
| Install | `pip install -e ".[dev]"` |
| Run tests | `pytest` |
| Lint | `ruff check .` |
| Format | `ruff format .` |

These are the same commands listed in `CLAUDE.md`, so Claude uses them too.

## Project Structure

```
claude-md-python-demo/
├── CLAUDE.md                       Project memory file that Claude loads each session
├── INSTRUCTIONS.md                 Condensed hands on walkthrough of the demo
├── README.md                       This file
├── The CLAUDE.md File.docx         The full written lesson
├── pyproject.toml                  Package metadata, dependencies, pytest and ruff config
├── .gitignore                      Ignores OS, editor, and Python build noise
├── .github/workflows/ci.yml        Runs ruff and pytest on every push
├── src/devhub/
│   ├── api/
│   │   └── config.py               Loads code-host tokens from the environment, never hardcoded
│   ├── auth/
│   │   └── webhook_auth.py         HMAC-SHA256 webhook signature validation
│   ├── integrations/
│   │   └── github_client.py        Reference code-host integration that follows CLAUDE.md
│   └── pipeline/                   Intentionally empty placeholder (see the note above)
├── tests/
│   ├── test_config.py
│   ├── test_webhook_auth.py
│   └── test_github_client.py
└── exercises/
    ├── README.md                                   Index, how to use, and key takeaways
    ├── 01-create-the-claude-md.md                  Read and understand the CLAUDE.md
    ├── 02-start-a-session.md                       Confirm the file loads automatically
    ├── 03-watch-claude-follow-your-conventions.md  Core exercise: the GitLab integration
    └── 04-capture-a-recurring-correction.md        Optional: save a correction to the file
```

## Branches

| Branch | Contents |
|---|---|
| `main` | The starting state for learners. No GitLab integration yet. |
| `solution/gitlab-integration` | A reference solution for Exercise 03: `gitlab_client.py` plus its tests. |

Try the exercise yourself before you look at the solution branch:

```bash
git diff main origin/solution/gitlab-integration
```

## Running the Demos

The demo is a guided Claude Code session rather than an application you launch. Follow
these steps in order. The `exercises/` folder expands each one with what to observe and
what to look for.

1. **Read the CLAUDE.md.** Open `CLAUDE.md` at the project root and read it top to
   bottom. Notice the project summary, the directory map, the commands, the code style
   rules, and the workflow. See `exercises/01-create-the-claude-md.md`.

2. **Start a session.** Open Claude Code in the project root so it loads the file:

   ```bash
   claude
   ```

   Then confirm the file was picked up by asking:

   ```
   What do you know about this project?
   ```

   Claude should summarise the stack, the directory map, and the conventions straight
   from `CLAUDE.md`. See `exercises/02-start-a-session.md`.

3. **Watch it follow your conventions.** Ask for a new feature without restating any
   rules:

   ```
   Add a new integration module for GitLab in src/devhub/integrations/
   ```

   Claude applies what the file already told it. It uses an HTTPS endpoint rather than
   plain `http://`, reads the token through `devhub.api.config` instead of hardcoding
   it, validates the caller's host and repo, adds type hints and an `__all__`
   declaration, and follows the explore, plan, implement workflow before adding a
   pytest test. None of that was in your request. See
   `exercises/03-watch-claude-follow-your-conventions.md`.

4. **Capture a recurring correction (optional).** Save a repeated correction back into
   the file so it sticks for next time:

   ```
   Add a note to CLAUDE.md: log API request URLs without their query string,
   since the query can contain a token.
   ```

   Claude updates `CLAUDE.md`, and from the next session that rule is part of its
   context automatically. See `exercises/04-capture-a-recurring-correction.md`.

## Exercises

The `exercises/` folder contains one guide per step of the demo, plus an index. Each
guide walks you from start to finish: what to do, what to observe, what to look for in
the code, and the intended learning outcome. Example prompts are quoted verbatim so
you can paste them into Claude Code exactly as written.

Start with [`exercises/README.md`](exercises/README.md), which explains how to use the
guides and lists the lesson's key takeaways, then work through the numbered files in
order.

## Additional Notes

- **Keep `CLAUDE.md` concise.** It is added to context every session, so every line
  costs something. Reference larger documents with the `@` symbol rather than pasting
  them, and capture only the rules that reflect real friction.
- **Never include secrets.** Treat `CLAUDE.md` as documentation that could be shared,
  since it becomes part of Claude's context. Keep API keys, credentials, and tokens
  out of it.
- **Bootstrap with `/init`.** In your own projects you can generate a starter
  `CLAUDE.md` with `/init`, then refine it. This demo writes one directly so the
  conventions are explicit.
- **Iterate.** The best `CLAUDE.md` files grow with the codebase. Use the `#` key or a
  quick request to Claude to append rules as you discover them.

### Troubleshooting

| Symptom | Resolution |
|---|---|
| Claude ignores the conventions | Confirm the file is named exactly `CLAUDE.md` and sits in the directory where you launched `claude`. |
| The file is getting long and unfocused | Move detailed sections into separate Markdown files and reference them with `@`. |
| A rule keeps being missed | Make it more specific and concrete. Vague guidance is easy to overlook. |
| `ModuleNotFoundError: No module named 'devhub'` | Activate the virtual environment and run `pip install -e ".[dev]"` from the repository root. |
