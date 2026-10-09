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
