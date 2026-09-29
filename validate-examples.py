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
    # The WHOLE line is returned; only the report shortens it (DETAIL_WIDTH). The caller
    # decides whether to retry as a fragment by searching this text, and a 200-char cut
    # made that decision depend on how long the file's PATH is: on the Linux CI runner
    # (/home/runner/work/...) six examples under the longest chapter directories lost
    # "can't appear at the top level" to the cut, were never retried, and failed CI on
    # every push from 2026-09-27 while passing on Windows.
    for ln in lines:
        if "error:" in ln:
            return False, ln
    for ln in lines:
        if "error" in ln.lower() or "panic" in ln.lower():
            return False, ln
    return False, (lines[-1] if lines else "non-zero exit, no output")


# ── FRAGMENTS (2026-09-26) ───────────────────────────────────────────────────────────
# ~220 of the book's examples are FRAGMENTS -- statements shown at top level, the way a
# chapter shows three lines to make a point -- and the compiler refuses them with "is a
# statement and can't appear at the top level" before it checks anything else. So a
# quarter of the book's code was never checked at all. A fragment is now retried with its
# top-level STATEMENTS moved into a synthesized `def main()` (declarations stay at top
# level), beside the original so `use` of a neighbouring module still resolves. A pass that
# needed this is reported separately ("as a fragment"), never silently as a whole program.
DETAIL_WIDTH = 200    # report text only; never cut a message before it is classified
FRAGMENT_SIGNS = ("can't appear at the top level", "unexpected top-level token")
DECL_WORDS = ("def ", "class ", "struct ", "union ", "enum ", "interface ", "mixin ",
              "extend ", "namespace ", "sig ", "type ", "use ", "extern ", "@", "cue ")


def wrap_fragment(text):
    """Top-level statements -> body of a synthesized main(); None if nothing to wrap."""
    if "def main(" in text:
        return None
    decls, body = [], []
    target = decls
    for ln in text.split("\n"):
        top = ln and not ln[0].isspace()
        if top and not ln.lstrip().startswith("#"):
            target = decls if ln.startswith(DECL_WORDS) else body
        (target.append(ln) if target is decls else target.append("    " + ln if ln.strip() else ""))
    if not any(b.strip() and not b.strip().startswith("#") for b in body):
        return None
    return "\n".join(decls).rstrip() + "\n\ndef main()\n" + "\n".join(body).rstrip() + "\n"


def compile_fragment(zebra, filepath, full):
    wrapped = wrap_fragment(filepath.read_text(encoding='utf-8', errors='replace'))
    if wrapped is None:
        return None
    tmp = filepath.with_name(filepath.stem + "__asfragment.zbr")
    try:
        tmp.write_text(wrapped, encoding='utf-8', newline='\n')
        return compile_example(zebra, tmp, full)
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass


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
    as_fragment = []
    detail = {}
    examples = [f for f in examples if not f.stem.endswith("__asfragment")]
    for i, f in enumerate(examples, 1):
        rel = f.relative_to(examples_dir).as_posix()
        ok, msg = compile_example(zebra, f, full)
        if not ok and any(s in msg for s in FRAGMENT_SIGNS):
            fr = compile_fragment(zebra, f, full)
            if fr is not None:
                ok, fmsg = fr
                if ok:
                    as_fragment.append(rel)
                else:
                    msg = "as a fragment inside main(): " + fmsg
        (passed if ok else failed).append(rel)
        if not ok:
            detail[rel] = msg[:DETAIL_WIDTH]
        if i % 50 == 0 or i == len(examples):
            print("  [" + str(i) + "/" + str(len(examples)) + "] " +
                  str(len(passed)) + " pass / " + str(len(failed)) + " fail")

    report = {
        "timestamp": datetime.now().isoformat(),
        "compiler": str(zebra),
        "total": len(examples),
        "passed": len(passed),
        "failed": len(failed),
        "passed_as_fragment": sorted(as_fragment),
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
          " | pass " + str(len(passed)) + " (" + str(len(as_fragment)) +
          " only as a fragment inside a synthesized main) | fail " + str(len(failed)))

    if update:
        baseline_path.write_text(
            "# Examples that compile cleanly. Regenerate with:\n"
            "#   python validate-examples.py " + ("--full " if full else "") + "--update-baseline\n"
            "# The gate fails when an entry here stops compiling.\n"
            "# Take it on a CASE-SENSITIVE filesystem (Linux / CI): on Windows `use Build`\n"
            "# resolves to a neighbouring build.zbr, so an example can pass there and fail\n"
            "# everywhere else (zebra-language BUG-450, found by this repo's CI on its first run).\n"
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
