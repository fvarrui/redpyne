import argparse
import json
import sys
from pathlib import Path

from .config import load_config
from .redmine import RedmineClient


def _resolve_paths(output_dir: str, issue_id: str) -> tuple[Path, Path]:
    """Return (json_path, attachments_dir) for the given issue."""
    base = Path(output_dir) / issue_id
    return base / "issue.json", base / "attachments"


def main():
    parser = argparse.ArgumentParser(
        prog="redpyne",
        description="Download a Redmine issue and its attachments.",
    )
    parser.add_argument("issue_id", help="Issue number (e.g. 123456)")
    parser.add_argument(
        "--output", default=".", metavar="DIR",
        help="Parent directory where the issue directory will be created (default: current directory).",
    )
    parser.add_argument("--url", metavar="URL", help="Redmine base URL (overrides config)")
    parser.add_argument("--username", metavar="USER", help="Redmine username (overrides config)")
    parser.add_argument("--password", metavar="PASS", help="Redmine password (overrides config)")
    parser.add_argument("--api-token", dest="api_token", metavar="TOKEN",
                        help="Redmine API token (overrides config)")
    args = parser.parse_args()

    try:
        cfg = load_config()
    except KeyError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    url = args.url or cfg.get("url")
    username = args.username or cfg.get("username")
    password = args.password or cfg.get("password")
    api_token = args.api_token or cfg.get("api_token")

    if not url:
        print(
            "Error: Redmine URL not provided. Use --url or set 'url' in ~/.redpyne/config.ini.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        client = RedmineClient(url=url, username=username, password=password, api_token=api_token)
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = client.get_issue(args.issue_id)
    except Exception as e:
        print(f"Failed to fetch issue {args.issue_id}: {e}", file=sys.stderr)
        sys.exit(1)

    json_path, attachments_dir = _resolve_paths(args.output, args.issue_id)

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {json_path}")

    attachments = data.get("issue", {}).get("attachments", [])
    if not attachments:
        return

    attachments_dir.mkdir(parents=True, exist_ok=True)
    for attachment in attachments:
        filename = attachment["filename"]
        dest = attachments_dir / filename
        try:
            client.download_file(attachment["content_url"], dest)
            print(f"Downloaded {dest}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}", file=sys.stderr)
