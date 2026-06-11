from pathlib import Path
import requests


class RedmineClient:
    def __init__(self, url: str, username: str = None, password: str = None, api_token: str = None):
        self.base_url = url.rstrip("/")
        self.session = requests.Session()
        if api_token:
            self.session.headers["X-Redmine-API-Key"] = api_token
        elif username and password:
            self.session.auth = (username, password)
        else:
            raise ValueError("Provide either api_token or username and password in the config.")

    def get_issue(self, issue_id: int | str) -> dict:
        response = self.session.get(
            f"{self.base_url}/issues/{issue_id}.json",
            params={"include": "attachments"},
        )
        response.raise_for_status()
        return response.json()

    def download_file(self, url: str, dest: Path) -> None:
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
