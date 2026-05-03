# Webspace Sync

A tool to synchronize files with a remote webspace via FTP_TLS.

![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
[![Lint](https://github.com/boxfritz-eu/webspace-sync/actions/workflows/lint.yml/badge.svg)](https://github.com/boxfritz-eu/webspace-sync/actions/workflows/lint.yml)
[![Mypy](https://github.com/boxfritz-eu/webspace-sync/actions/workflows/mypy.yml/badge.svg)](https://github.com/boxfritz-eu/webspace-sync/actions/workflows/mypy.yml)
[![Bandit](https://github.com/boxfritz-eu/webspace-sync/actions/workflows/bandit.yml/badge.svg)](https://github.com/boxfritz-eu/webspace-sync/actions/workflows/bandit.yml)
[![Tests](https://github.com/boxfritz-eu/webspace-sync/actions/workflows/tests.yml/badge.svg)](https://github.com/boxfritz-eu/webspace-sync/actions/workflows/tests.yml)

## Installation

```bash
uv sync
```

## Configuration

Create a `config/secrets.yaml` file with your FTP credentials:

```yaml
webspace:
  ftp:
    host: ftp.example.com
    username: your_username
    password: your_password
```

## Usage

### Command Line Interface

You can run the tool using `uv run webspace_sync`.

#### Upload a file

```bash
uv run webspace_sync upload path/to/local/file.json --remote-dir data/raw
```

#### List remote files

```bash
uv run webspace_sync ls data/raw
```

#### Push a directory

```bash
uv run webspace_sync push ./local_dir data/remote_dir --recurse --force --delete
```

- `--recurse`: Push directories recursively.
- `--force`: Always replace files on the remote target, even if the local version is older.
- `--delete`: Delete files on the remote target that don't exist locally.

#### Pull a directory

```bash
uv run webspace_sync pull data/remote_dir ./local_dir --recurse --force --delete
```

- `--recurse`: Pull directories recursively.
- `--force`: Always replace local files with the remote versions, even if the local files are newer.
- `--delete`: Delete local files that don't exist on the remote server.

#### Sync a directory (bidirectional)

```bash
uv run webspace_sync sync ./local_dir data/remote_dir --recurse --resolve remote
```

- `--recurse`: Sync directories recursively.
- `--force`: Force overwrite on both sides.
- `--delete`: Delete unmatched files on both sides.
- `--resolve`: Conflict resolution strategy (`local`, `remote`, `new`, `old`, `skip`).

### Python API

You can also use the `WebspaceClient` in your Python code:

```python
from webspace_sync import WebspaceClient
from pathlib import Path

client = WebspaceClient(host="ftp.example.com", username="user", password="pass")

with client:
    # Upload with force and delete
    client.upload(Path("local_file.txt"), "remote/dir", force=True, delete=True)

    # Push/Pull with new options
    client.push(Path("./local_dir"), "remote/dir", recursive=True, force=True, delete=True)
    client.pull("remote/dir", Path("./local_dir"), recursive=True, force=True, delete=True)

    # Bidirectional sync with conflict resolution
    client.sync(Path("./local_dir"), "remote/dir", recursive=True, resolve="remote")

    files = client.ls("remote/dir")
    print(files)
```

## Development

### Running tests

```bash
uv run pytest
```
