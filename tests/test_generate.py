"""Tests for reporium-roadmap generate.py."""

from __future__ import annotations

import json

import httpx
import respx

from generate import (
    _fetch_repo_stats,
    _format_item,
    build_readme,
    load_roadmap,
)

GITHUB_API = "https://api.github.com/repos"


# ── load_roadmap ──────────────────────────────────────────────────────────────


def test_load_roadmap(tmp_path, monkeypatch):
    """Parses roadmap.json correctly."""
    data = {"vision": "test", "live": [], "in_progress": []}
    (tmp_path / "roadmap.json").write_text(json.dumps(data))
    monkeypatch.chdir(tmp_path)
    result = load_roadmap()
    assert result["vision"] == "test"


# ── _fetch_repo_stats ─────────────────────────────────────────────────────────


@respx.mock
async def test_fetch_repo_stats_success():
    """Returns correct stats dict on 200."""
    url = f"{GITHUB_API}/perditioinc/reporium"
    respx.get(url).mock(
        return_value=httpx.Response(
            200,
            json={
                "pushed_at": "2026-03-16T10:00:00Z",
                "open_issues_count": 3,
                "stargazers_count": 42,
            },
        )
    )
    stats = await _fetch_repo_stats("tok", "perditioinc/reporium")
    assert stats is not None
    assert stats["exists"] is True
    assert stats["last_commit"] == "2026-03-16"
    assert stats["stars"] == 42
    assert stats["open_issues"] == 3


@respx.mock
async def test_fetch_repo_stats_404_returns_placeholder():
    """Returns placeholder dict with exists=False on 404 — no crash."""
    url = f"{GITHUB_API}/perditioinc/missing-repo"
    respx.get(url).mock(return_value=httpx.Response(404))
    stats = await _fetch_repo_stats("tok", "perditioinc/missing-repo")
    assert stats is not None
    assert stats["exists"] is False


@respx.mock
async def test_fetch_repo_stats_network_error_returns_none():
    """Returns None gracefully on network error."""
    url = f"{GITHUB_API}/perditioinc/reporium"
    respx.get(url).mock(side_effect=httpx.ConnectError("timeout"))
    stats = await _fetch_repo_stats("tok", "perditioinc/reporium")
    assert stats is None


# ── _format_item ──────────────────────────────────────────────────────────────


def test_format_item_with_live_stats(sample_stats):
    """Shows last commit, stars, and issues when stats are available."""
    item = {"name": "reporium", "repo": "perditioinc/reporium", "description": "AI tool"}
    result = _format_item(item, sample_stats)
    assert "2026-03-16" in result
    assert "42" in result
    assert "3 open issues" in result


def test_format_item_404_repo():
    """Shows '(repo not yet public)' placeholder for 404 repos."""
    item = {"name": "private-repo", "repo": "org/private", "description": "private"}
    stats = {"exists": False, "last_commit": None, "open_issues": 0, "stars": 0}
    result = _format_item(item, stats)
    assert "not yet public" in result


def test_format_item_none_stats():
    """Shows '(data unavailable)' when stats fetch failed."""
    item = {"name": "repo", "repo": "org/repo", "description": "desc"}
    result = _format_item(item, None)
    assert "unavailable" in result


def test_format_item_with_url():
    """Item with url field uses it as the link target."""
    item = {"name": "reporium", "url": "https://reporium.com", "description": "AI tool"}
    result = _format_item(item, None)
    assert "reporium.com" in result


# ── build_readme (legacy structure) ──────────────────────────────────────────


def test_build_readme_has_all_sections(sample_roadmap, sample_stats):
    """Legacy README contains all four section headings."""
    stats_map = {
        "perditioinc/reporium": sample_stats,
        "perditioinc/reporium-db": sample_stats,
    }
    readme = build_readme(sample_roadmap, stats_map, "2026-03-17")
    assert "## Live" in readme
    assert "## In Progress" in readme
    assert "## Coming Next" in readme
    assert "## Backlog" in readme


def test_build_readme_contains_vision(sample_roadmap):
    """README contains the vision statement."""
    readme = build_readme(sample_roadmap, {}, "2026-03-17")
    assert "10K repos by March 2026" in readme


def test_build_readme_shows_live_stats(sample_roadmap, sample_stats):
    """README shows live commit date for repos with stats."""
    stats_map = {"perditioinc/reporium": sample_stats}
    readme = build_readme(sample_roadmap, stats_map, "2026-03-17")
    assert "2026-03-16" in readme


def test_build_readme_shows_coming_next_no_stats(sample_roadmap):
    """Coming next items appear without live stats."""
    readme = build_readme(sample_roadmap, {}, "2026-03-17")
    assert "repo-intelligence" in readme


def test_build_readme_shows_backlog(sample_roadmap):
    """Backlog items appear in README."""
    readme = build_readme(sample_roadmap, {}, "2026-03-17")
    assert "reporium enterprise" in readme


def test_build_readme_has_changelog_link(sample_roadmap):
    """README links to CHANGELOG.md."""
    readme = build_readme(sample_roadmap, {}, "2026-03-17")
    assert "CHANGELOG.md" in readme


# ── build_readme (new current_state structure) ───────────────────────────────


def test_build_readme_new_structure_has_current_state(new_roadmap):
    """New structure README contains Current State section."""
    readme = build_readme(new_roadmap, {}, "2026-03-18")
    assert "## Current State" in readme
    assert "### Working" in readme
    assert "### Not Working" in readme


def test_build_readme_new_structure_shows_honest_status(new_roadmap):
    """New structure README shows what is not working."""
    readme = build_readme(new_roadmap, {}, "2026-03-18")
    assert "ingestion" in readme.lower()
    assert "## Fixing Now" in readme


def test_build_readme_new_structure_has_deadline(new_roadmap):
    """New structure README shows next_up with deadline."""
    readme = build_readme(new_roadmap, {}, "2026-03-18")
    assert "March" in readme


def test_build_readme_new_structure_has_changelog(new_roadmap):
    """New structure README contains changelog entries."""
    readme = build_readme(new_roadmap, {}, "2026-03-18")
    assert "## Changelog" in readme
    assert "v0.3.0" in readme
