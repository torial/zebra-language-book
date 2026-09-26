#!/usr/bin/env python3
"""
Zebra Programming Book - Code Example Validator

Compiles every extracted example with the real Zebra compiler and gates on
REGRESSION against a baseline, in the same style as the language repo's
tools/full_sweep.sh.

    python validate-examples.py                    # validate; exit 1 on regression
    python validate-examples.py --update-baseline  # re-lock the passing set
    python validate-examples.py --full [--update-baseline]
        # a REAL build (`zebra -c --check-full`: front end + Zig analysis, not run) of every example that has a `main`, against
        # its own baseline (validation-baseline-full.txt). Slower -- zig runs per file.

WHAT THE DEFAULT RUN PROVES, AND WHAT IT DOES NOT (2026-09-25). It runs `zebra -c`: the
front end only -- parse, resolve, type-check -- with no Zig build and no run. So it cannot
see an example whose emitted Zig does not build (the book itself documents several), and it
cannot see a WRONG OUTPUT COMMENT: ch06 promised `H` from `text[0].toString()` while the
program printed `72`, and every run of this validator passed it. `--full` closes the first
gap. Nothing here closes the second; that takes running the program and comparing.

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
BASELINE_FULL = REPO / "validation-baseline-full.txt"


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


def compile_example(zebra: Path, filepath: Path, full: bool = False):
    """Return (ok, detail). The compiler is the only judge — no pre-filtering."""
    # `-c --check-full`, never `--check-full` alone: before rc3 the bare flag compiled
    # AND RAN the program, so a "full check" of every example would start the book's
    # HTTP server and open its GUI windows. The explicit pair is safe on every release.
    mode = ["-c", "--check-full"] if full else ["-c"]
    limit = 300 if full else 60
    try:
        r = subprocess.run([str(zebra), *mode, str(filepath)],
                           capture_output=True, text=True, timeout=limit,
                           encoding='utf-8', errors='replace')
    except subprocess.TimeoutExpired:
        return False, "compilation timeout (>" + str(limit) + "s)"
    except Exception as e:  # noqa: BLE001 - report, don't crash the sweep
        return False, "harness error: " + str(e)
    if r.returncode == 0:
        return True, ""
    out = ((r.stderr or "") + (r.stdout or "")).strip()
    lines = [ln.strip() for ln in out.split("\n") if ln.strip()]
    # Prefer the compiler's own `error:` line. The old rule took the first line mentioning
    # "error" anywhere, else the FIRST line -- which is the `compiling: <path>` banner, so
    # 15 failure records said nothing about why they failed.
    for ln in lines:
        if "error:" in ln:
            return False, ln[:200]
    for ln in lines:
        if "error" in ln.lower() or "panic" in ln.lower():
            return False, ln[:200]
    return False, (lines[-1][:200] if lines else "non-zero exit, no output")


def load_baseline(path):
    if not path.exists():
        return None
    return {ln.strip() for ln in path.read_text(encoding='utf-8').split("\n")
            if ln.strip() and not ln.startswith("#")}


def main() -> int:
    update = "--update-baseline" in sys.argv
    full = "--full" in sys.argv
    baseline_path = BASELINE_FULL if full else BASELINE
    zebra = find_compiler()
    examples_dir = REPO / "examples"
    examples = sorted(examples_dir.rglob("*.zbr"))
    if full:
        # Only programs with an entry point can be built; fragments are the -c run's job.
        examples = [f for f in examples
                    if "def main(" in f.read_text(encoding='utf-8', errors='replace')]

    print("=" * 70)
    print("Zebra Programming Book - Code Example Validator")
    print("=" * 70)
    print("compiler: " + str(zebra))
    print("mode:     " + ("--check-full (real build, programs with a main)" if full
                          else "-c (front end only: no Zig build, no run)"))
    if not examples:
        print("\n[FAIL] No examples found in " + str(examples_dir) +
              "\n       Run `python extract-examples.py` first.")
        return 1
    print("examples: " + str(len(examples)) + "\n")

    passed, failed = [], []
    detail = {}
    for i, f in enumerate(examples, 1):
        rel = f.relative_to(examples_dir).as_posix()
        ok, msg = compile_example(zebra, f, full)
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
    report_stem = "validation-report-full" if full else "validation-report"
    (REPO / (report_stem + ".json")).write_text(
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
    (REPO / (report_stem + ".txt")).write_text(
        "\n".join(lines) + "\n", encoding='utf-8', newline='\n')

    print("\nTotal " + str(len(examples)) +
          " | pass " + str(len(passed)) + " | fail " + str(len(failed)))

    if update:
        baseline_path.write_text(
            "# Examples that compile cleanly. Regenerate with:\n"
            "#   python validate-examples.py " + ("--full " if full else "") + "--update-baseline\n"
            "# The gate fails when an entry here stops compiling.\n"
            + "\n".join(sorted(passed)) + "\n", encoding='utf-8', newline='\n')
        print("baseline updated: " + str(len(passed)) + " passing examples")
        return 0

    base = load_baseline(baseline_path)
    if base is None:
        print("\n[WARN] no " + baseline_path.name + " — nothing to gate against.")
        print("       Create one with: python validate-examples.py " + ("--full " if full else "") + "--update-baseline")
        return 0

    # A regression is an example that STILL EXISTS and has stopped compiling. A baselined
    # file that no longer exists is not one: an unnamed block is named by a hash of its
    # content, so "gone" means its text was edited or it was removed -- its new text is
    # judged afresh. The old rule counted every vanished file as a regression, and with
    # positional names one inserted block made that fire for every block after it.
    #
    # THE COLLAPSE GUARD is what makes that safe: if most of the baseline vanished at once,
    # the extractor has broken, and "nothing regressed" would be a vacuous pass.
    present = {f.relative_to(examples_dir).as_posix() for f in examples}
    gone = sorted(base - present)
    if base and len(gone) > max(25, len(base) // 4):
        print("\n[REFUSED] " + str(len(gone)) + " of " + str(len(base)) +
              " baselined examples no longer exist -- the extraction has probably broken,"
              " so no regression verdict can be given. Re-run extract-examples.py and look.")
        return 2
    if gone:
        print("\n[info] " + str(len(gone)) + " baselined example(s) no longer exist (their "
              "text changed or the block was removed); not counted as regressions:")
        for g in gone[:10]:
            print("   " + g)
    regressed = sorted((base & present) - set(passed))
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
