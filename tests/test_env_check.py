"""Smoke tests for the environment verification module.

These must not require any third-party packages beyond stdlib — they exercise
the ``env_check`` logic that *reports* on the environment.
"""

from __future__ import annotations

from dcat.scripts import env_check


def test_env_check_returns_tuple():
    ok, report = env_check.check_environment()
    assert isinstance(ok, bool)
    assert isinstance(report, str)
    assert "DCAT Environment Verification" in report


def test_env_check_report_lists_dependencies():
    _, report = env_check.check_environment()
    # The report should mention key packages.
    for package in ("torch", "numpy"):
        assert package in report


def test_env_check_reports_cuda_status():
    ok, report = env_check.check_environment()
    assert ok is True or "MISSING" in report
    assert "CUDA available" in report
