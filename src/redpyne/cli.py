import argparse
import json
import sys
from pathlib import Path

from .config import load_config
from .redmine import RedmineClient


def main():
    parser = argparse.ArgumentParser(
        prog="redpyne",
        description="Download a Redmine issue and its attachments.",
    )
    parser.add_argument("issue_id", help="Issue number (e.g. 123456)")
    args = parser.parse_args()

    try:
        cfg = load_config()
    except (FileNotFoundError, KeyError) as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        client = RedmineClient(
            url=cfg["url"],
            username=cfg.get("username"),
            password=cfg.get("password"),
            api_token=cfg.get("api_token"),
        )
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = client.get_issue(args.issue_id)
    except Exception as e:
        print(f"Failed to fetch issue {args.issue_id}: {e}", file=sys.stderr)
        sys.exit(1)

    json_path = Path(f"{args.issue_id}.json")
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {json_path}")

    attachments = data.get("issue", {}).get("attachments", [])
    if not attachments:
        return

    attachments_dir = Path("attachments")
    attachments_dir.mkdir(exist_ok=True)

    for attachment in attachments:
        filename = attachment["filename"]
        url = attachment["content_url"]
        dest = attachments_dir / filename
        try:
            client.download_file(url, dest)
            print(f"Downloaded {dest}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}", file=sys.stderr)
