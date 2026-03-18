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
