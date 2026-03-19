"""Shared fixtures for reporium-roadmap tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_roadmap() -> dict:
    """A minimal roadmap dict for testing."""
    return {
        "vision": "Track every AI tool. 10K repos by March 2026.",
        "live": [
            {
                "name": "reporium",
                "repo": "perditioinc/reporium",
                "description": "AI tool discovery",
                "url": "https://reporium.com",
            }
        ],
        "in_progress": [
            {
                "name": "reporium-db",
                "repo": "perditioinc/reporium-db",
                "description": "Nightly sync",
            }
        ],
        "coming_next": [{"name": "repo-intelligence", "description": "Scoring library"}],
        "backlog": [{"name": "reporium enterprise", "description": "Self-hosted"}],
    }


@pytest.fixture
def sample_stats() -> dict:
    """Realistic stats dict for a live repo."""
    return {
        "exists": True,
        "last_commit": "2026-03-16",
        "open_issues": 3,
        "stars": 42,
    }


@pytest.fixture
def new_roadmap() -> dict:
    """Roadmap using the new current_state structure."""
    return {
        "vision": "Track every AI tool. 10K repos by March 2026.",
        "version": "v0.3.0",
        "current_state": {
            "working": [
                {
                    "name": "reporium.com",
                    "repo": "perditioinc/reporium",
                    "url": "https://reporium.com",
                    "evidence": "Live — 818 repos browseable",
                }
            ],
            "not_working": [
                {
                    "name": "reporium-ingestion",
                    "reason": "Pipeline not running — 0 categories enriched",
                }
            ],
        },
        "fixing_now": [
            {
                "name": "forksync SYNC_REPORT.md",
                "description": "Workflow fix deployed — unblocks metrics",
            }
        ],
        "next_up": {
            "deadline": "end of March 2026",
            "items": ["10K repos tracked"],
        },
        "future": {
            "deadline": "end of April 2026",
            "items": ["100K repos"],
        },
        "coming_next": [{"name": "repo-intelligence", "description": "Scoring library"}],
        "changelog": [
            {"version": "v0.3.0", "date": "2026-03-18", "notes": "6 new repos built"},
        ],
    }
