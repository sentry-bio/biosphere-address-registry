from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_local_conformance import run  # noqa: E402


def test_complete_example_graph_conforms(tmp_path):
    result = run(tmp_path / "registry")
    assert result["ok"] is True
    assert result["ingested"] == 9
    assert result["graph"]["graph_checked"] is True
    assert result["graph"]["errors"] == []
    assert all(result["semantic_checks"].values())
