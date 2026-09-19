#!/usr/bin/env python3
"""Regression suite for .claude/hooks/pre_tool_use.py.

Runs the real script as a subprocess, feeding it JSON payloads via stdin,
exactly like Claude Code does. Exit code 2 means blocked, 0 means allowed.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK_PATH = REPO_ROOT / ".claude" / "hooks" / "pre_tool_use.py"

CASES = [
    ("git commit -m \"x\"", "main", 2),
    ("git add . && git commit -m \"x\"", "main", 2),
    ("git -C . commit -m \"x\"", "main", 2),
    ("git status", "main", 0),
    ("git log", "main", 0),
    ('echo "git commit" > f.txt', "main", 0),
    ("git commit -m \"x\"", "feature/x", 0),
]


def run_hook(command, cwd):
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}, "cwd": cwd})
    result = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=payload,
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.returncode


def setup_repo(base_dir):
    repo = Path(base_dir)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "init"], cwd=repo, check=True)
    subprocess.run(["git", "branch", "feature/x"], cwd=repo, check=True)
    return repo


def main():
    with tempfile.TemporaryDirectory() as base_dir:
        repo = setup_repo(base_dir)

        failures = []
        for command, branch, expected in CASES:
            subprocess.run(["git", "checkout", "-q", branch], cwd=repo, check=True)
            actual = run_hook(command, str(repo))
            status = "PASS" if actual == expected else "FAIL"
            if status == "FAIL":
                failures.append((command, branch, expected, actual))
            print(f"[{status}] `{command}` on `{branch}` -> exit {actual} (expected {expected})")

        if failures:
            print(f"\n{len(failures)} case(s) failed.")
            sys.exit(1)

        print(f"\nAll {len(CASES)} cases passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
