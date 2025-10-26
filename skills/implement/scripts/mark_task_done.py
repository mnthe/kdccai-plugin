#!/usr/bin/env python3
"""
Mark a task as completed in a plan document.

Usage:
    python mark_task_done.py <plan_file> <task_number>

Example:
    python mark_task_done.py docs/plans/PLN-001-2025-10-26-report.md 1
"""

import sys
import re
from pathlib import Path


def mark_task_done(plan_file: Path, task_number: int) -> bool:
    """
    Mark a task as done by checking its checkbox.

    Args:
        plan_file: Path to the plan markdown file
        task_number: Task number to mark as done (1-indexed)

    Returns:
        True if task was found and marked, False otherwise
    """
    if not plan_file.exists():
        print(f"Error: Plan file not found: {plan_file}")
        return False

    content = plan_file.read_text(encoding="utf-8")

    # Find the task section
    task_pattern = rf"### Task {task_number}:.*?(?=\n### Task |\n## |\Z)"
    task_match = re.search(task_pattern, content, re.DOTALL)

    if not task_match:
        print(f"Error: Task {task_number} not found in {plan_file}")
        return False

    # Replace unchecked boxes with checked boxes in this task only
    task_content = task_match.group(0)
    updated_task = re.sub(r"- \[ \]", "- [x]", task_content)

    # Replace in original content
    updated_content = content.replace(task_content, updated_task)

    # Write back
    plan_file.write_text(updated_content, encoding="utf-8")

    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python mark_task_done.py <plan_file> <task_number>")
        print("Example: python mark_task_done.py docs/plans/PLN-001-2025-10-26-report.md 1")
        sys.exit(1)

    plan_file = Path(sys.argv[1])
    task_number = int(sys.argv[2])

    if mark_task_done(plan_file, task_number):
        print(f"✅ Marked Task {task_number} as completed in {plan_file.name}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
