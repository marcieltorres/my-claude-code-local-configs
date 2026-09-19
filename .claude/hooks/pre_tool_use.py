#!/usr/bin/env python3
"""PreToolUse hook dispatcher.

Reads a tool-call payload from stdin, runs each rule in RULES against it, and
blocks the first one that returns a reason. Exit code 2 blocks the tool call
and shows the printed stderr message to Claude; exit code 0 allows it.

Structure inspired by:
https://github.com/disler/claude-code-hooks-mastery/blob/main/.claude/hooks/pre_tool_use.py
"""

import json
import os
import shlex
import subprocess
import sys

PROTECTED_BRANCHES = {"main", "master"}
SEPARATORS = {"&&", "||", ";", "|"}
FLAGS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree"}
TERRAFORM_DESTRUCTIVE_SUBCOMMANDS = {"apply", "destroy"}


def split_on_separators(tokens):
    """Split a token list into segments on shell separators (&&, ||, ;, |)."""
    segments = []
    current = []
    for token in tokens:
        if token in SEPARATORS:
            segments.append(current)
            current = []
        else:
            current.append(token)
    segments.append(current)
    return segments


def is_git_commit_invocation(segment):
    """Check whether a token segment is a `git ... commit ...` invocation."""
    if not segment or segment[0] != "git":
        return False
    i = 1
    while i < len(segment):
        arg = segment[i]
        if arg in FLAGS_WITH_VALUE:
            i += 2
            continue
        if arg.startswith("-"):
            i += 1
            continue
        return arg == "commit"
    return False


def command_has_git_commit(command):
    """Check whether any segment of a shell command is a git commit invocation."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return False
    return any(is_git_commit_invocation(segment) for segment in split_on_separators(tokens))


def is_terraform_destructive_invocation(segment):
    """Check whether a token segment is a `terraform apply`/`terraform destroy` invocation."""
    if not segment or segment[0] != "terraform":
        return False
    i = 1
    while i < len(segment):
        arg = segment[i]
        if arg.startswith("-"):
            i += 1
            continue
        return arg in TERRAFORM_DESTRUCTIVE_SUBCOMMANDS
    return False


def command_has_terraform_destructive(command):
    """Check whether any segment of a shell command is a terraform apply/destroy invocation."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return False
    return any(is_terraform_destructive_invocation(segment) for segment in split_on_separators(tokens))


def get_current_branch(cwd):
    """Return the current git branch name for cwd, or None if it can't be determined."""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def check_no_commit_on_main(tool_name, tool_input, cwd):
    """Block `git commit` when the current branch is main or master."""
    if tool_name != "Bash":
        return None

    command = tool_input.get("command", "")
    if not command or not command_has_git_commit(command):
        return None

    branch = get_current_branch(cwd)
    if not branch or branch not in PROTECTED_BRANCHES:
        return None

    return (
        f"Direct commit to '{branch}' is blocked by hook. "
        "Create a branch (git checkout -b <name>) and commit there, then open a PR."
    )


def check_no_terraform_apply_or_destroy(tool_name, tool_input, cwd):
    """Block `terraform apply` and `terraform destroy`, regardless of branch."""
    if tool_name != "Bash":
        return None

    command = tool_input.get("command", "")
    if not command or not command_has_terraform_destructive(command):
        return None

    return (
        "`terraform apply`/`terraform destroy` is blocked by hook. "
        "Run it manually outside of Claude Code, with explicit review."
    )


RULES = [check_no_commit_on_main, check_no_terraform_apply_or_destroy]


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    cwd = input_data.get("cwd") or os.getcwd()

    for rule in RULES:
        try:
            reason = rule(tool_name, tool_input, cwd)
        except Exception:
            # A broken rule fails open — it must never block unrelated work.
            continue
        if reason:
            print(f"BLOCKED: {reason}", file=sys.stderr)
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
