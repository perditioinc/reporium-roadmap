"""Generate roadmap README.md with live GitHub repo stats."""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com/repos"
TIMEOUT = 15


def load_roadmap(path: str = "roadmap.json") -> dict[str, Any]:
    """Load roadmap configuration from JSON file.

    Args:
        path: Path to roadmap.json.

    Returns:
        Parsed roadmap dict.
    """
    return json.loads(open(path, encoding="utf-8").read())


async def _fetch_repo_stats(token: str, owner_repo: str) -> Optional[dict[str, Any]]:
    """Fetch basic stats for a GitHub repo via REST API.

    Args:
        token: GitHub personal access token.
        owner_repo: e.g. 'perditioinc/reporium'.

    Returns:
        Dict with keys: last_commit, open_issues, stars, exists.
        Returns placeholder dict with exists=False on 404.
        Returns None on other errors.
    """
    url = f"{GITHUB_API}/{owner_repo}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(url, headers=headers)
        if resp.status_code == 404:
            logger.warning("Repo %s not found (404)", owner_repo)
            return {"exists": False, "last_commit": None, "open_issues": 0, "stars": 0}
        resp.raise_for_status()
        data = resp.json()
        return {
            "exists": True,
            "last_commit": (data.get("pushed_at") or "")[:10],
            "open_issues": data.get("open_issues_count", 0),
            "stars": data.get("stargazers_count", 0),
        }
    except Exception as exc:  # noqa: BLE001
        logger.warning("Error fetching %s: %s", owner_repo, exc)
        return None


def _format_item(item: dict, stats: Optional[dict]) -> str:
    """Format a single roadmap item as a markdown list entry.

    Args:
        item: Roadmap item dict (name, description, optional repo/url/version/features).
        stats: Live GitHub stats dict or None.

    Returns:
        Markdown list item string.
    """
    name = item["name"]
    version = item.get("version", "")
    description = item.get("description", "")
    url = item.get("url", "")
    repo = item.get("repo", "")
    features = item.get("features", [])

    name_with_version = f"{name} {version}" if version else name

    if url:
        label = f"[**{name_with_version}**]({url})"
    elif repo:
        label = f"[**{name_with_version}**](https://github.com/{repo})"
    else:
        label = f"**{name_with_version}**"

    if stats is None:
        status_str = "_(data unavailable)_"
    elif not stats.get("exists", True):
        status_str = "_(repo not yet public)_"
    else:
        last = stats.get("last_commit") or "—"
        stars = stats.get("stars", 0)
        issues = stats.get("open_issues", 0)
        status_str = f"last commit: `{last}` · {stars} stars · {issues} open issues"

    lines = [f"- {label} — {description}  \n  {status_str}"]
    if features:
        feature_str = " · ".join(features)
        lines.append(f"  _{feature_str}_")

    return "\n".join(lines)


def _section(title: str, items: list[dict], stats_map: dict[str, Optional[dict]]) -> str:
    """Render a roadmap section as markdown.

    Args:
        title: Section heading text.
        items: List of roadmap item dicts.
        stats_map: Mapping of owner/repo → stats dict (or None).

    Returns:
        Markdown section string.
    """
    lines = [f"## {title}", ""]
    for item in items:
        repo = item.get("repo", "")
        stats = stats_map.get(repo) if repo else None
        lines.append(_format_item(item, stats))
    return "\n".join(lines)


def _plain_section(title: str, items: list[dict]) -> str:
    """Render a roadmap section without live stats (coming_next, backlog).

    Args:
        title: Section heading text.
        items: List of roadmap item dicts.

    Returns:
        Markdown section string.
    """
    lines = [f"## {title}", ""]
    for item in items:
        name = item["name"]
        repo = item.get("repo", "")
        description = item.get("description", "")
        if repo:
            label = f"[**{name}**](https://github.com/{repo})"
        else:
            label = f"**{name}**"
        lines.append(f"- {label} — {description}")
    return "\n".join(lines)


def _changelog_section() -> str:
    """Read and include CHANGELOG.md content.

    Returns:
        Markdown changelog section string.
    """
    path = "CHANGELOG.md"
    try:
        content = open(path, encoding="utf-8").read()
        return "## Changelog\n\n" + content
    except Exception:  # noqa: BLE001
        return ""


def build_readme(roadmap: dict, stats_map: dict[str, Optional[dict]], generated_at: str) -> str:
    """Assemble the full README from roadmap data and live stats.

    Args:
        roadmap: Parsed roadmap.json dict.
        stats_map: Mapping of owner/repo → GitHub stats.
        generated_at: ISO-8601 generation timestamp.

    Returns:
        Complete README.md markdown string.
    """
    vision = roadmap.get("vision", "")
    platform_version = roadmap.get("version", "")
    live_section = _section("Live", roadmap.get("live", []), stats_map)
    in_progress_section = _section("In Progress", roadmap.get("in_progress", []), stats_map)
    coming_next_section = _plain_section("Coming Next", roadmap.get("coming_next", []))
    backlog_section = _plain_section("Backlog", roadmap.get("backlog", []))
    changelog = _changelog_section()

    version_line = f"Platform **{platform_version}** · " if platform_version else ""

    return f"""# Reporium Roadmap

> {vision}

---

{live_section}

---

{in_progress_section}

---

{coming_next_section}

---

{backlog_section}

---

{changelog}

---

*{version_line}Last updated: {generated_at[:10]} · See [CHANGELOG.md](CHANGELOG.md) for version history.*
"""


async def main() -> None:
    """Fetch live stats for all repos in roadmap.json and generate README.md."""
    t0 = time.monotonic()

    token = os.getenv("GH_TOKEN", "")
    if not token:
        raise ValueError("GH_TOKEN is required")

    roadmap = load_roadmap()

    # Collect all repos that have a 'repo' field
    all_items = roadmap.get("live", []) + roadmap.get("in_progress", [])
    repos = [item["repo"] for item in all_items if item.get("repo")]

    # Fetch stats concurrently (with simple semaphore for courtesy)
    import asyncio

    sem = asyncio.Semaphore(5)

    async def _with_sem(repo: str) -> tuple[str, Optional[dict]]:
        """Fetch stats for one repo under semaphore."""
        async with sem:
            stats = await _fetch_repo_stats(token, repo)
        return repo, stats

    results = await asyncio.gather(*[_with_sem(r) for r in repos])
    stats_map: dict[str, Optional[dict]] = dict(results)

    generated_at = datetime.now(timezone.utc).isoformat()
    readme = build_readme(roadmap, stats_map, generated_at)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    elapsed = time.monotonic() - t0
    logger.info("Roadmap README generated in %.2fs", elapsed)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
