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
_DB_INDEX_URL = "https://raw.githubusercontent.com/perditioinc/reporium-db/main/data/index.json"


async def _fetch_db_stats(token: str) -> dict[str, Any]:
    """Fetch live stats from reporium-db index.json.

    Returns:
        Dict with db_total (int) and db_languages (int). Falls back to 0 on error.
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(_DB_INDEX_URL, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        meta = data.get("meta", {})
        return {
            "db_total": meta.get("total", 0),
            "db_languages": len(data.get("languages", {})),
        }
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to fetch reporium-db index: %s", exc)
        return {"db_total": 0, "db_languages": 0}


def _apply_context(text: str, context: dict[str, Any]) -> str:
    """Substitute {db_total} / {db_languages} placeholders in a string."""
    try:
        return text.format(**context)
    except (KeyError, ValueError):
        return text


def _apply_context_to_items(items: list[dict], context: dict[str, Any]) -> list[dict]:
    """Return a copy of items with template placeholders substituted."""
    result = []
    for item in items:
        copy = dict(item)
        for field in ("evidence", "description", "reason", "notes"):
            if field in copy and isinstance(copy[field], str):
                copy[field] = _apply_context(copy[field], context)
        result.append(copy)
    return result


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


def _current_state_section(roadmap: dict, stats_map: dict[str, Optional[dict]]) -> str:
    """Render the current state section with working / not working subsections.

    Args:
        roadmap: Parsed roadmap.json dict.
        stats_map: Mapping of owner/repo → GitHub stats.

    Returns:
        Markdown section string.
    """
    state = roadmap.get("current_state", {})
    working = state.get("working", [])
    not_working = state.get("not_working", [])

    lines = ["## Current State", ""]

    if working:
        lines.append("### Working")
        lines.append("")
        for item in working:
            repo = item.get("repo", "")
            name = item["name"]
            evidence = item.get("evidence", "")
            url = item.get("url", "")
            stats = stats_map.get(repo)

            if url:
                label = f"[**{name}**]({url})"
            elif repo:
                label = f"[**{name}**](https://github.com/{repo})"
            else:
                label = f"**{name}**"

            if stats and stats.get("exists", True):
                last = stats.get("last_commit") or "—"
                stars = stats.get("stars", 0)
                stat_str = f"last commit: `{last}` · {stars} stars"
            else:
                stat_str = ""

            stat_suffix = f"  \n  {stat_str}" if stat_str else ""
            lines.append(f"- {label} — {evidence}{stat_suffix}")
        lines.append("")

    if not_working:
        lines.append("### Not Working")
        lines.append("")
        for item in not_working:
            name = item["name"]
            reason = item.get("reason", "")
            repo = item.get("repo", "")
            if repo:
                label = f"[**{name}**](https://github.com/{repo})"
            else:
                label = f"**{name}**"
            lines.append(f"- {label} — {reason}")

    return "\n".join(lines)


def _fixing_now_section(items: list[dict]) -> str:
    """Render the 'Fixing Now' section."""
    lines = ["## Fixing Now", ""]
    for item in items:
        name = item["name"]
        description = item.get("description", "")
        lines.append(f"- **{name}** — {description}")
    return "\n".join(lines)


def _next_up_section(data: dict) -> str:
    """Render the 'Next Up' section with deadline."""
    deadline = data.get("deadline", "")
    items = data.get("items", [])
    lines = [f"## Next Up — {deadline}" if deadline else "## Next Up", ""]
    for item in items:
        lines.append(f"- {item}")
    return "\n".join(lines)


def _future_section(data: dict) -> str:
    """Render the 'Target' section."""
    deadline = data.get("deadline", "")
    items = data.get("items", [])
    lines = [f"## Target: {deadline}" if deadline else "## Future", ""]
    for item in items:
        lines.append(f"- {item}")
    return "\n".join(lines)


def _changelog_from_roadmap(changelog: list[dict]) -> str:
    """Render changelog from roadmap.json entries."""
    if not changelog:
        return _changelog_section()
    lines = ["## Changelog", ""]
    for entry in changelog:
        version = entry.get("version", "")
        date = entry.get("date", "")
        notes = entry.get("notes", "")
        lines.append(f"### {version} - {date}")
        lines.append(f"{notes}")
        lines.append("")
    return "\n".join(lines)


def build_readme(roadmap: dict, stats_map: dict[str, Optional[dict]], generated_at: str) -> str:
    """Assemble the full README from roadmap data and live stats.

    Supports both the new structure (current_state, fixing_now, next_up, future)
    and the legacy structure (live, in_progress, coming_next, backlog).

    Args:
        roadmap: Parsed roadmap.json dict.
        stats_map: Mapping of owner/repo → GitHub stats.
        generated_at: ISO-8601 generation timestamp.

    Returns:
        Complete README.md markdown string.
    """
    vision = roadmap.get("vision", "")
    platform_version = roadmap.get("version", "")
    version_line = f"Platform **{platform_version}** · " if platform_version else ""

    # New structure
    if "current_state" in roadmap:
        current = _current_state_section(roadmap, stats_map)
        fixing = _fixing_now_section(roadmap.get("fixing_now", []))
        next_up = _next_up_section(roadmap.get("next_up", {}))
        future = _future_section(roadmap.get("future", {}))
        coming = _plain_section("Coming Next", roadmap.get("coming_next", []))
        changelog = _changelog_from_roadmap(roadmap.get("changelog", []))

        return f"""# Reporium Roadmap

> {vision}

---

{current}

---

{fixing}

---

{next_up}

---

{future}

---

{coming}

---

{changelog}

---

*{version_line}Last updated: {generated_at[:10]} · See [CHANGELOG.md](CHANGELOG.md) for version history.*
"""

    # Legacy structure (live, in_progress, coming_next, backlog)
    live_section = _section("Live", roadmap.get("live", []), stats_map)
    in_progress_section = _section("In Progress", roadmap.get("in_progress", []), stats_map)
    coming_next_section = _plain_section("Coming Next", roadmap.get("coming_next", []))
    backlog_section = _plain_section("Backlog", roadmap.get("backlog", []))
    changelog = _changelog_section()

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

    import asyncio

    # Fetch live reporium-db stats for template substitution
    context = await _fetch_db_stats(token)

    # Apply live context to all text fields that contain placeholders
    state = roadmap.get("current_state", {})
    if state:
        roadmap = dict(roadmap)
        roadmap["current_state"] = {
            "working": _apply_context_to_items(state.get("working", []), context),
            "not_working": _apply_context_to_items(state.get("not_working", []), context),
        }

    # Collect all repos that have a 'repo' field across all sections
    all_items: list[dict] = []
    state = roadmap.get("current_state", {})
    all_items += state.get("working", [])
    all_items += state.get("not_working", [])
    all_items += roadmap.get("fixing_now", [])
    all_items += roadmap.get("live", [])
    all_items += roadmap.get("in_progress", [])
    repos = list({item["repo"] for item in all_items if item.get("repo")})

    # Fetch GitHub stats concurrently
    sem = asyncio.Semaphore(5)

    async def _with_sem(repo: str) -> tuple[str, Optional[dict]]:
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
