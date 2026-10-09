# Exercise 02: Start a Session

Now that the `CLAUDE.md` is in place, confirm that Claude Code actually loads it. The
whole value of the file is that it loads on its own, so this exercise proves the
mechanism before you rely on it.

## What to Do

1. Open Claude Code in the project root so it loads the file:

   ```bash
   claude
   ```

2. Ask Claude what it already knows, without pasting anything from the file:

   ```
   What do you know about this project?
   ```

## What to Observe

Claude should summarise the stack, the directory map, and the conventions straight
from your `CLAUDE.md`, without you pasting anything. Look for these details in its
answer:

- It is a developer-productivity platform for software engineering teams, a Python
  backend that pulls pull-request data from code hosts and feeds an ML model that
  flags risky changes for review.
- The directory map: `src/devhub/auth/`, `src/devhub/integrations/`,
  `src/devhub/pipeline/`, `src/devhub/api/`, and `tests/`.
- The commands: `pip install -e ".[dev]"`, `pytest`, `ruff check .`, and
  `ruff format .`.
- The code style rules, including HTTPS only endpoints, type hints, `__all__`, and no
  hardcoded tokens.

If Claude produces this summary from a cold start, the file was picked up correctly.

## What to Look for in the Code

There is nothing to change here. The point of the exercise is that Claude answered
from the `CLAUDE.md` alone. Compare its summary line by line against the file you read
in Exercise 01 and confirm that everything it said traces back to a line in that file
rather than to a guess about the code.

If the summary is missing or wrong, check the troubleshooting notes in the root
[README](../README.md): confirm the file is named exactly `CLAUDE.md` and that it
sits in the directory where you launched `claude`.

## Learning Outcome

Project memory is automatic. You did not attach the file, paste its contents, or
remind Claude of anything. Once `CLAUDE.md` is at the project root, every session
starts with that context already loaded. This is the foundation the next exercise
builds on.

Continue to [Exercise 03](03-watch-claude-follow-your-conventions.md).
