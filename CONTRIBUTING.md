# Contributing to POLARIS

**Evidence:** IMPLEMENTED (process). Product features remain DESIGNED.

## Before you write code

1. Read [README.md](README.md) and [README_ARCHITECTURE.md](README_ARCHITECTURE.md).
2. Check [MASTER_CURSOR_PROMPT.md](MASTER_CURSOR_PROMPT.md) for the current priority (P0 vs later).
3. Open a focused branch from `main` (`feature/…`, `fix/…`, `docs/…`).
4. Follow [README_WORKFLOW.md](README_WORKFLOW.md).

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
make test
make lint
```

Optional C++ placeholder:

```bash
make test-cpp
```

## Commits and PRs

- Conventional Commits
- Draft PRs welcome; mark ready when DoD is met
- Template: `.github/pull_request_template.md`
- CODEOWNERS will request review from `@HCHAPS404`

## Owners (RACI minimum)

| Area | Responsible | Accountable |
|------|-------------|-------------|
| Architecture / platform | Helmut | Helmut |
| Horizon / Vector / Forge UX | Laura | Helmut |
| Hazards / country research | Lenin | Helmut |
| Merge to `main` | Reviewer on CODEOWNERS | Helmut |

## Security

Report vulnerabilities privately per [SECURITY.md](SECURITY.md). Never open a public issue with credentials.

## License

By contributing you agree that your work is licensed under Apache-2.0 ([LICENSE](LICENSE)).
