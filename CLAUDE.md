# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**redpyne** is a Python CLI tool for downloading issues from Redmine. For each issue it creates a directory `<id>/` containing `issue.json` and an `attachments/` subdirectory with any attached files.

## Commands

```bash
# Install (editable) — also installs the `requests` dependency
pip install -e .

# Run the CLI
redpyne 123456
```

## Configuration

User configuration lives at `~/.redpyne/config.ini`:

```ini
[redmine]
url = https://your-redmine-instance.example.com
; use either api_token or username + password
api_token = your_api_token
; username = your_username
; password = your_password
```

## Architecture

```
src/redpyne/
  __init__.py   — package version
  cli.py        — entry point (`main()`); argument parsing and orchestration
  config.py     — reads ~/.redpyne/config.ini via configparser
  redmine.py    — RedmineClient: fetches issue JSON and downloads attachments
```

The entry point is `redpyne.cli:main`, wired via `[project.scripts]` in `pyproject.toml`. The build backend is `hatchling` with `packages = ["src/redpyne"]`.

**Authentication**: `RedmineClient` accepts either `api_token` (sent as `X-Redmine-API-Key` header) or `username`/`password` (HTTP Basic Auth). The API call includes `?include=attachments` to retrieve attachment metadata in a single request; each attachment is then downloaded by its `content_url`.

**Output paths** (`_resolve_paths` in `cli.py`): always creates `<output>/<id>/issue.json` and `<output>/<id>/attachments/`. `--output` defaults to `.` (current directory).

Config file is optional; all fields (`url`, `username`, `password`, `api_token`) can be overridden via CLI flags. If the file is absent, a dict is returned and the CLI validates that the minimum required fields are present.
