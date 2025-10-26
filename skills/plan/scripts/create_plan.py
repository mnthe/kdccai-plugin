#!/usr/bin/env python3
"""
Create a new plan file from template.

Usage:
    python create_plan.py <plan_id> <plan_name> [project_root]

Example:
    python create_plan.py PLN-001 "daily-report-automation"
    python create_plan.py PLN-002 "excel-data-merger" /path/to/project
"""

import sys
from pathlib import Path
from datetime import date


def create_plan_file(plan_id: str, plan_name: str, template_content: str, project_root: Path, user_name: str = "user") -> Path:
    """
    Create a new plan file from template.

    Args:
        plan_id: Plan ID (e.g., PLN-001)
        plan_name: Plan name (e.g., daily-report-automation)
        template_content: Content of the plan template
        project_root: Path to the project root directory

    Returns:
        Path to the created plan file
    """
    # Ensure plans directory exists
    plans_dir = project_root / "docs" / "plans"
    plans_dir.mkdir(parents=True, exist_ok=True)

    # Create filename: PLN-XXX-YYYY-MM-DD-name.md
    today = date.today().strftime("%Y-%m-%d")
    filename = f"{plan_id}-{today}-{plan_name}.md"
    plan_path = plans_dir / filename

    # Replace placeholders in template
    content = template_content.replace("{{PLAN_ID}}", plan_id)
    content = content.replace("{{DATE}}", today)
    content = content.replace("{{PLAN_NAME}}", plan_name.replace("-", " ").title())
    content = content.replace("{{USER_NAME}}", user_name)

    # Write plan file
    plan_path.write_text(content, encoding="utf-8")

    return plan_path


def main():
    if len(sys.argv) < 3:
        print("Usage: python create_plan.py <plan_id> <plan_name> [project_root]")
        print("Example: python create_plan.py PLN-001 daily-report-automation")
        sys.exit(1)

    plan_id = sys.argv[1]
    plan_name = sys.argv[2]

    # Get project root from argument or use current directory
    if len(sys.argv) > 3:
        project_root = Path(sys.argv[3]).resolve()
    else:
        project_root = Path.cwd()

    # Template will be provided by the skill when this script is called
    # This is a fallback template for standalone usage
    template_content = """# {{PLAN_NAME}}

**Plan ID**: {{PLAN_ID}}
**Date**: {{DATE}}
**Status**: Draft

## Requirements

### What to Build

[Describe what you want to build]

### Why

[Explain why you need this]

### Success Criteria

[How will you know it works?]

## Scenarios

### SCN-001: [Scenario Name]

**Description**: [What happens in this scenario]

**Input**: [What data/files are needed]

**Expected Output**: [What should happen]

**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Tasks

### Task 1: [Task Name]

**Related Scenario**: SCN-001

**Description**: [What to implement]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Task 2: [Task Name]

**Related Scenario**: SCN-001

**Description**: [What to implement]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Notes

[Any additional notes, constraints, or considerations]
"""

    # Create plan file
    plan_path = create_plan_file(plan_id, plan_name, template_content, project_root)

    print(f"✅ Created plan: {plan_path}")
    print(f"\nNext steps:")
    print(f"1. Edit the plan file to fill in requirements and scenarios")
    print(f"2. Use 'implement' skill to start implementing tasks")


if __name__ == "__main__":
    main()
