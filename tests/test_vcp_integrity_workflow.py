from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "vcp-integrity.yml"


def text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_workflow_exists_and_is_read_only() -> None:
    data = text()
    assert "name: VCP integrity" in data
    assert "permissions:\n  contents: read" in data
    assert "persist-credentials: false" in data
    assert "timeout-minutes: 10" in data


def test_pull_requests_are_bound_to_exact_head_sha() -> None:
    data = text()
    assert "EXPECTED_SHA: ${{ github.event.pull_request.head.sha || github.sha }}" in data
    assert "ref: ${{ env.EXPECTED_SHA }}" in data
    assert 'test "$actual" = "$EXPECTED_SHA"' in data


def test_full_suite_and_native_project_regressions_are_required() -> None:
    data = text()
    assert 'python -m unittest discover -s tests -p "test_*.py" -v' in data
    assert "tests.test_native_project_source_integrity_contract" in data
    assert "tests.test_native_project_v2_pack_reproducibility" in data
    assert "tests.test_native_project_v2_safe_replacement" in data
    assert "tests.test_native_project_v2_task_closeout" in data


def test_package_rebuild_and_kernel_ceiling_are_required() -> None:
    data = text()
    assert "build_native_project_successor_v2a1.py" in data
    assert 'assert actual_sha == expected["sha256"]' in data
    assert "assert len(kernel) <= 8000" in data
    assert 'assert len(kernel) == manifest["native_kernel_chars"]' in data


def test_workflow_runs_for_relevant_pr_main_and_manual_events() -> None:
    data = text()
    assert "pull_request:" in data
    assert "push:" in data
    assert "workflow_dispatch:" in data
    assert '"project-instructions/**"' in data
    assert '"tools/**"' in data
    assert '"tests/**"' in data
