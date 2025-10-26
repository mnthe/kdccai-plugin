#!/usr/bin/env python3
"""
Update plan document status in YAML frontmatter.

Usage:
    python update_plan_status.py <plan_file> <new_status>

Example:
    python update_plan_status.py docs/plans/PLN-001-2025-10-26-report.md completed
    python update_plan_status.py docs/plans/PLN-001-2025-10-26-report.md blocked

Valid statuses: pending, in_progress, completed, blocked
"""

import sys
import re
from pathlib import Path
from datetime import date


def update_plan_status(plan_file: Path, new_status: str) -> bool:
    """
    Update plan status in YAML frontmatter.

    Args:
        plan_file: Path to the plan markdown file
        new_status: New status (pending, in_progress, completed, blocked)

    Returns:
        True if status was updated, False otherwise
    """
    valid_statuses = ['pending', 'in_progress', 'completed', 'blocked']

    if new_status not in valid_statuses:
        print(f"Error: Invalid status '{new_status}'. Must be one of: {', '.join(valid_statuses)}")
        return False

    if not plan_file.exists():
        print(f"Error: Plan file not found: {plan_file}")
        return False

    content = plan_file.read_text(encoding="utf-8")

    # Check if file has YAML frontmatter
    if not content.startswith('---'):
        print(f"Error: Plan file does not have YAML frontmatter")
        return False

    # Extract frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"Error: Invalid YAML frontmatter format")
        return False

    frontmatter = parts[1]
    body = parts[2]

    # Update status
    updated_frontmatter = re.sub(
        r'status:\s*\w+',
        f'status: {new_status}',
        frontmatter
    )

    # Update updated date
    today = date.today().strftime("%Y-%m-%d")
    updated_frontmatter = re.sub(
        r'updated:\s*[\d-]+',
        f'updated: {today}',
        updated_frontmatter
    )

    # If status is completed, update verified
    if new_status == 'completed':
        updated_frontmatter = re.sub(
            r'verified:\s*\w+',
            'verified: true',
            updated_frontmatter
        )
        updated_frontmatter = re.sub(
            r'verification_date:\s*\S+',
            f'verification_date: {today}',
            updated_frontmatter
        )

    # Reconstruct file
    updated_content = f"---{updated_frontmatter}---{body}"

    # Write back
    plan_file.write_text(updated_content, encoding="utf-8")

    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python update_plan_status.py <plan_file> <new_status>")
        print("Example: python update_plan_status.py docs/plans/PLN-001-2025-10-26-report.md completed")
        print("Valid statuses: pending, in_progress, completed, blocked")
        sys.exit(1)

    plan_file = Path(sys.argv[1])
    new_status = sys.argv[2]

    if update_plan_status(plan_file, new_status):
        print(f"✅ Updated plan status to '{new_status}' in {plan_file.name}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
