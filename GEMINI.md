# Webspace Sync - Project Context

## Project Overview

`webspace-sync` is a Python-based utility designed to synchronize files and directories with a remote webspace using FTP_TLS. It leverages the `pyftpsync` library for robust synchronization logic and provides both a Command Line Interface (CLI) and a Python API (`WebspaceClient`).

### Core Technologies

- **Language:** Python (>= 3.13)
- **Package Management:** `uv`
- **Synchronization:** `pyftpsync`
- **Configuration:** `python-box`, `PyYAML`
- **Task Runner:** `go-task` (via `Taskfile.yml`)

## Building and Running

### Installation

The project uses `uv` for dependency management.

```bash
# Install dependencies and sync environment
uv sync
# OR
task install
```

### Running the CLI

The CLI entry point is `webspace_sync`.

```bash
# Run via uv
uv run webspace_sync --help

# Run via Taskfile
task run -- --help
```

### Common Commands (via Taskfile)

- `task install`: Sync dependencies.
- `task test`: Run the full `pytest` suite.
- `task test-cov`: Run tests with coverage report.
- `task lint`: Lint code using `ruff` and apply safe fixes.
- `task format`: Format code using `ruff`.
- `task check`: Run both linting and formatting checks.
- `task all`: Run check and test-cov.
- `task bump-patch|minor|major`: Version bumping via `bump-my-version`.

## Development Conventions & Best Practices

### Python Coding Standards (from AGENTS.md)

- **Typing:** Use type hints (PEP 484) for all functions and variables. Prefer native types (e.g., `dict` instead of `Dict`).
- **Design Principles:**
  - **SOLID:** Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.
  - **DRY:** Don't Repeat Yourself. Abstract repeated logic into reusable components.
- **Docstrings:** Use Google-style docstrings (PEP 257) for all modules, classes, and functions.
- **Zen of Python:** Adhere to the principles of "The Zen of Python" (e.g., "Readability counts", "Explicit is better than implicit").

### Quality & Security Tools

- **Linting & Formatting:** `ruff` is used for both. Run `uv run ruff check .` and `uv run ruff format .`.
- **Type Checking:** `mypy` is used for static analysis. Run `python -m mypy src/`.
- **Security:** `bandit` is used for security linting. Run `bandit -r .`.
- **Pre-commit:** Hooks are configured to run `ruff`, `mypy`, and other checks on every commit.

### Testing Strategy

- **Framework:** `pytest` is the preferred framework.
- **Location:** Tests reside in `tests/`, named `test_*.py`.
- **Mocking:** Use `unittest.mock` to isolate tests from FTP and filesystem side effects.
- **Coverage:** Aim for high coverage, using `task test-cov` to monitor.

## Architecture

- `src/webspace_sync/client.py`: Core `WebspaceClient` implementation.
- `src/webspace_sync/__init__.py`: CLI entry point and argument parsing.
- `tests/`: Project tests.

## Node.js Best Practices (Project Standard)

Although primarily a Python project, the following Node.js standards apply if applicable:

- **Package Manager:** `npm`.
- **Testing:** `vitest`.
- **Linting/Formatting:** `ESLint` and `Prettier`.
- **Build Tool:** `Vite`.
- **Modules:** Use ES Modules (`"type": "module"`).

## Configuration

- Use `config/secrets.yaml` for credentials (based on `config/secrets-example.yaml`).
- **Safety:** Never commit `config/secrets.yaml`.
