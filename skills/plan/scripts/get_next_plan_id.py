#!/usr/bin/env python3
"""
Get the next Plan ID by scanning existing plan files in docs/plans/.

Usage:
    python get_next_plan_id.py [project_root]

Returns the next available Plan ID (e.g., PLN-001, PLN-002, ...).
If no plans exist, returns PLN-001.
"""

import sys
from pathlib import Path
import re


def get_next_plan_id(project_root: Path) -> str:
    """
    Scan docs/plans/ directory and return the next available Plan ID.

    Args:
        project_root: Path to the project root directory

    Returns:
        Next Plan ID in format PLN-XXX (e.g., PLN-001, PLN-002)
    """
    plans_dir = project_root / "docs" / "plans"

    # If plans directory doesn't exist, start with PLN-001
    if not plans_dir.exists():
        return "PLN-001"

    # Find all plan files matching PLN-XXX pattern
    plan_pattern = re.compile(r"PLN-(\d{3})")
    max_id = 0

    for plan_file in plans_dir.glob("PLN-*.md"):
        match = plan_pattern.search(plan_file.name)
        if match:
            plan_num = int(match.group(1))
            max_id = max(max_id, plan_num)

    # Return next ID
    next_id = max_id + 1
    return f"PLN-{next_id:03d}"


def main():
    # Get project root from argument or use current directory
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1]).resolve()
    else:
        project_root = Path.cwd()

    # Get and print next Plan ID
    next_id = get_next_plan_id(project_root)
    print(next_id)


if __name__ == "__main__":
    main()
