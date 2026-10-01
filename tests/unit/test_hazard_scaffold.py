"""Generator creates a real placeholder package."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "generators" / "hazard"))

from scaffold import scaffold  # noqa: E402


def test_scaffold_demo_hazard() -> None:
    # Run against the real repo but unique name, then clean up.
    name = "zz_p0_scaffold_demo"
    hazard_dir = ROOT / "hazards" / name
    test_file = ROOT / "tests" / "unit" / "hazards" / f"test_{name}_placeholder.py"
    config = ROOT / "configs" / "hazards" / f"{name}.yaml"
    schema = ROOT / "schemas" / "hazard" / f"{name}.yaml"
    try:
        created = scaffold(name, force=True)
        assert any(p.name == "placeholder.py" for p in created)
        assert (hazard_dir / "interface.py").is_file()
        assert (hazard_dir / "provenance.json").is_file()
        assert config.is_file()
        sys.path.insert(0, str(hazard_dir))
        import placeholder as plugin  # type: ignore

        assert plugin.describe()["evidence"] == "PLACEHOLDER"
    finally:
        shutil.rmtree(hazard_dir, ignore_errors=True)
        for p in (test_file, config, schema):
            if p.exists():
                p.unlink()
