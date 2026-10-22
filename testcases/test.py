#!/usr/bin/env python3
"""Run the public testcases against the interpreter.

Usage:
    python3 testcases/test.py [path/to/code] [--timeout SECONDS]

If no executable is given, this script tries, in order:
    ./code, build/code (from the repository root), testcases/code

Build the interpreter first with:
    cmake -B build
    cmake --build build
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SUITES = (
    ("Basic Test", "basic-testcases", "test*.in"),
    ("Big Integer Test", "bigint-testcases", "BigIntegerTest*.in"),
)


def natural_key(path):
    """Sort test10 after test9 instead of after test1."""
    return [
        (0, int(part)) if part.isdigit() else (1, part)
        for part in re.split(r"(\d+)", path.name)
    ]


def find_executable(given):
    if given is not None:
        executable = Path(given).expanduser()
        if not executable.is_file():
            sys.exit(f"error: executable not found: {executable}")
        return executable.resolve()

    for candidate in (
        Path.cwd() / "code",
        REPO_ROOT / "build" / "code",
        SCRIPT_DIR / "code",
    ):
        if candidate.is_file():
            return candidate.resolve()

    sys.exit(
        "error: interpreter executable not found.\n"
        "Build it first (cmake -B build && cmake --build build), "
        "or pass its path explicitly:\n"
        "    python3 testcases/test.py path/to/code"
    )


def first_difference(expected, actual):
    expected_lines = expected.splitlines(keepends=True)
    actual_lines = actual.splitlines(keepends=True)
    for number, (want, got) in enumerate(zip(expected_lines, actual_lines), 1):
        if want != got:
            return f"line {number}: expected {want!r}, got {got!r}"
    if len(expected_lines) != len(actual_lines):
        return f"expected {len(expected_lines)} lines, got {len(actual_lines)}"
    return "outputs differ"


def run_case(executable, input_path, timeout):
    """Return None on success, or a human-readable failure reason."""
    expected_path = input_path.with_suffix(".out")
    if not expected_path.is_file():
        return f"missing expected output: {expected_path.name}"

    try:
        with input_path.open("rb") as stdin:
            process = subprocess.run(
                [str(executable)],
                stdin=stdin,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
    except subprocess.TimeoutExpired:
        return f"timed out after {timeout:g}s"
    except OSError as error:
        return f"could not run executable: {error}"

    if process.returncode != 0:
        reason = f"exit code {process.returncode}"
        stderr = process.stderr.decode(errors="replace").strip()
        if stderr:
            reason += f"; stderr: {stderr.splitlines()[0][:200]}"
        return reason

    expected = expected_path.read_bytes()
    if process.stdout != expected:
        return first_difference(
            expected.decode(errors="replace"),
            process.stdout.decode(errors="replace"),
        )
    return None


def main():
    parser = argparse.ArgumentParser(description="Run the public testcases.")
    parser.add_argument(
        "executable",
        nargs="?",
        help="path to the built interpreter (default: ./code or build/code)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        metavar="SECONDS",
        help="per-case timeout in seconds (default: 30)",
    )
    args = parser.parse_args()

    executable = find_executable(args.executable)
    print(f"Interpreter: {executable}")

    total = 0
    passed = 0
    failures = []

    for title, directory, pattern in SUITES:
        cases = sorted((SCRIPT_DIR / directory).glob(pattern), key=natural_key)
        if not cases:
            print(f"\n[{title}] no testcases found in {SCRIPT_DIR / directory}")
            continue

        print(f"\n[{title}] {len(cases)} cases")
        for input_path in cases:
            total += 1
            name = input_path.stem
            reason = run_case(executable, input_path, args.timeout)
            if reason is None:
                passed += 1
                print(f"  PASS  {name}")
            else:
                failures.append((title, name, reason))
                print(f"  FAIL  {name}: {reason}")

    print(f"\n{passed}/{total} passed")
    if failures:
        print("Failed cases:")
        for title, name, reason in failures:
            print(f"  {title}/{name}: {reason}")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        sys.exit(130)
