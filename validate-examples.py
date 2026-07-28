#!/usr/bin/env python3
"""
Zebra Programming Book - Code Example Validator

Compiles every extracted example with the real Zebra compiler and gates on
REGRESSION against a baseline, in the same style as the language repo's
tools/full_sweep.sh.

    python validate-examples.py                    # validate; exit 1 on regression
    python validate-examples.py --update-baseline  # re-lock the passing set

Why a baseline instead of "everything must pass": `examples/` is extracted from
the book's code blocks, and many blocks are legitimately not standalone programs
(fragments illustrating one line, deliberately-wrong "mistake" examples, or one
half of a two-module example). Requiring 100% would make the gate permanently
red and therefore ignored. The baseline is the allow-list of what currently
compiles; the gate fails only when something that used to compile stops.

History / why this file was rewritten (2026-07-27)
--------------------------------------------------
The previous version could not fail. It ran a `validate_syntax` pre-check that
required both `class ` and `def ` to appear in a file before it would attempt
compilation; most examples satisfy neither, so they were marked *skipped* and
never compiled. The checked-in report read:

    Total examples:  180
    Passed:          0
    Failed:          0
    Skipped:         180

Zero passed, zero failed - a green-looking report from a harness that had never
compiled a single line. It also invoked a bare `zebra` from PATH, which is not
where the compiler lives on this machine. Both are fixed here: the compiler is
located explicitly, and the compiler itself is the only judge of validity.

Outputs: validation-report.json, validation-report.txt, validation-baseline.txt
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:  # Windows consoles default to cp1252 and choke on the status glyphs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

REPO = Path(__file__).resolve().parent
BASELINE = REPO / "validation-baseline.txt"


def find_compiler() -> Path:
    """Locate the Zebra compiler. $ZEBRA wins, then PATH, then the sibling repo."""
    env = os.environ.get("ZEBRA")
    if env and Path(env).exists():
        return Path(env)
    on_path = shutil.which("zebra") or shutil.which("zebra.exe")
    if on_path:
        return Path(on_path)
    sibling = REPO.parent / "zebra-language" / "zig-out" / "bin" / "zebra.exe"
    if sibling.exists():
        return sibling
    raise SystemExit(
        "validate-examples: cannot find the Zebra compiler.\n"
        "  Set $ZEBRA, put `zebra` on PATH, or build ../zebra-language "
        "(zig build).")


def compile_example(zebra: Path, filepath: Path):
    """Return (ok, detail). The compiler is the only judge — no pre-filtering."""
    try:
        r = subprocess.run([str(zebra), "-c", str(filepath)],
                           capture_output=True, text=True, timeout=60,
                           encoding='utf-8', errors='replace')
    except subprocess.TimeoutExpired:
        return False, "compilation timeout (>60s)"
    except Exception as e:  # noqa: BLE001 - report, don't crash the sweep
        return False, "harness error: " + str(e)
    if r.returncode == 0:
        return True, ""
    out = ((r.stderr or "") + (r.stdout or "")).strip()
    for line in out.split("\n"):
        if "error" in line.lower():
            return False, line.strip()[:200]
    return False, out.split("\n")[0][:200] if out else "non-zero exit"


def load_baseline():
    if not BASELINE.exists():
        return None
    return {ln.strip() for ln in BASELINE.read_text(encoding='utf-8').split("\n")
            if ln.strip() and not ln.startswith("#")}


def main() -> int:
    update = "--update-baseline" in sys.argv
    zebra = find_compiler()
    examples_dir = REPO / "examples"
    examples = sorted(examples_dir.rglob("*.zbr"))

    print("=" * 70)
    print("Zebra Programming Book - Code Example Validator")
    print("=" * 70)
    print("compiler: " + str(zebra))
    if not examples:
        print("\n[FAIL] No examples found in " + str(examples_dir) +
              "\n       Run `python extract-examples.py` first.")
        return 1
    print("examples: " + str(len(examples)) + "\n")

    passed, failed = [], []
    detail = {}
    for i, f in enumerate(examples, 1):
        rel = f.relative_to(examples_dir).as_posix()
        ok, msg = compile_example(zebra, f)
        (passed if ok else failed).append(rel)
        if not ok:
            detail[rel] = msg
        if i % 50 == 0 or i == len(examples):
            print("  [" + str(i) + "/" + str(len(examples)) + "] " +
                  str(len(passed)) + " pass / " + str(len(failed)) + " fail")

    report = {
        "timestamp": datetime.now().isoformat(),
        "compiler": str(zebra),
        "total": len(examples),
        "passed": len(passed),
        "failed": len(failed),
        "failures": detail,
    }
    (REPO / "validation-report.json").write_text(
        json.dumps(report, indent=2), encoding='utf-8', newline='\n')

    lines = ["ZEBRA PROGRAMMING BOOK - EXAMPLE VALIDATION REPORT",
             "=" * 70, "",
             "Generated: " + report["timestamp"],
             "Compiler:  " + str(zebra), "",
             "Total:  " + str(report["total"]),
             "Passed: " + str(report["passed"]),
             "Failed: " + str(report["failed"]), ""]
    if detail:
        lines += ["FAILURES", "-" * 70]
        for k in sorted(detail):
            lines.append("  " + k)
            lines.append("      " + detail[k])
    (REPO / "validation-report.txt").write_text(
        "\n".join(lines) + "\n", encoding='utf-8', newline='\n')

    print("\nTotal " + str(len(examples)) +
          " | pass " + str(len(passed)) + " | fail " + str(len(failed)))

    if update:
        BASELINE.write_text(
            "# Examples that compile cleanly. Regenerate with:\n"
            "#   python validate-examples.py --update-baseline\n"
            "# The gate fails when an entry here stops compiling.\n"
            + "\n".join(sorted(passed)) + "\n", encoding='utf-8', newline='\n')
        print("baseline updated: " + str(len(passed)) + " passing examples")
        return 0

    base = load_baseline()
    if base is None:
        print("\n[WARN] no validation-baseline.txt — nothing to gate against.")
        print("       Create one with: python validate-examples.py --update-baseline")
        return 0

    regressed = sorted(base - set(passed))
    if regressed:
        print("\n[FAIL] " + str(len(regressed)) +
              " example(s) that used to compile no longer do:")
        for r in regressed[:25]:
            print("   " + r + "\n       " + detail.get(r, "(no longer present)"))
        if len(regressed) > 25:
            print("   ... and " + str(len(regressed) - 25) + " more")
        return 1

    gained = sorted(set(passed) - base)
    if gained:
        print("\n[OK] no regressions. " + str(len(gained)) +
              " newly-passing example(s) — run --update-baseline to lock them in.")
    else:
        print("\n[OK] no regressions vs baseline (" + str(len(base)) + " examples).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
