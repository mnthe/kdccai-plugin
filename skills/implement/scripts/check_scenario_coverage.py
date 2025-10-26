#!/usr/bin/env python3
"""
Check if all scenarios in a plan have corresponding tests with pytest markers.

Usage:
    python check_scenario_coverage.py <plan_file> [project_root]

Example:
    python check_scenario_coverage.py docs/plans/PLN-001-2025-10-26-report.md
    python check_scenario_coverage.py docs/plans/PLN-001-2025-10-26-report.md /path/to/project
"""

import sys
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Set


def extract_scenarios_from_plan(plan_file: Path) -> List[str]:
    """
    Extract scenario IDs from plan document.

    Args:
        plan_file: Path to the plan markdown file

    Returns:
        List of scenario IDs (e.g., ['SCN-001', 'SCN-002'])
    """
    if not plan_file.exists():
        raise FileNotFoundError(f"Plan file not found: {plan_file}")

    content = plan_file.read_text(encoding="utf-8")

    # Find all SCN-XXX patterns
    scenario_pattern = re.compile(r'SCN-(\d{3})')
    matches = scenario_pattern.findall(content)

    # Deduplicate and sort
    scenario_ids = sorted(set(f"SCN-{num}" for num in matches))

    return scenario_ids


def find_tests_with_marker(marker: str, tests_dir: Path) -> List[str]:
    """
    Find test files containing a specific pytest marker.

    Args:
        marker: Pytest marker to search for (e.g., 'scn001')
        tests_dir: Path to tests directory

    Returns:
        List of test file paths containing the marker
    """
    if not tests_dir.exists():
        return []

    matching_files = []

    # Search for @pytest.mark.<marker> in all test files
    pattern = f"@pytest\\.mark\\.{marker}"

    for test_file in tests_dir.glob("test_*.py"):
        content = test_file.read_text(encoding="utf-8")
        if re.search(pattern, content):
            matching_files.append(str(test_file))

    return matching_files


def run_tests_for_marker(marker: str) -> Dict[str, any]:
    """
    Run pytest for a specific marker and return results.

    Args:
        marker: Pytest marker to run (e.g., 'scn001')

    Returns:
        Dict with 'passed', 'failed', 'error' counts
    """
    try:
        result = subprocess.run(
            ['pytest', '-m', marker, '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout + result.stderr

        # Parse pytest output for results
        passed = len(re.findall(r'PASSED', output))
        failed = len(re.findall(r'FAILED', output))

        return {
            'passed': passed,
            'failed': failed,
            'returncode': result.returncode,
            'output': output
        }
    except subprocess.TimeoutExpired:
        return {'passed': 0, 'failed': 0, 'returncode': -1, 'output': 'Timeout'}
    except Exception as e:
        return {'passed': 0, 'failed': 0, 'returncode': -1, 'output': str(e)}


def check_coverage(plan_file: Path, project_root: Path) -> None:
    """
    Check scenario coverage for a plan.

    Args:
        plan_file: Path to the plan markdown file
        project_root: Path to the project root directory
    """
    print(f"Checking scenario coverage for: {plan_file.name}\n")

    # Extract scenarios from plan
    scenarios = extract_scenarios_from_plan(plan_file)

    if not scenarios:
        print("⚠️  No scenarios found in plan document")
        return

    print(f"Found {len(scenarios)} scenario(s): {', '.join(scenarios)}\n")

    tests_dir = project_root / "tests"

    if not tests_dir.exists():
        print(f"⚠️  Tests directory not found: {tests_dir}")
        print("   No tests have been written yet.")
        return

    # Check coverage for each scenario
    results = []
    uncovered = []
    failed_scenarios = []

    for scenario_id in scenarios:
        # Convert SCN-001 to scn001 for pytest marker
        marker = scenario_id.lower().replace('-', '')

        # Find tests with this marker
        test_files = find_tests_with_marker(marker, tests_dir)

        if not test_files:
            print(f"⚠️  {scenario_id}: No tests found")
            uncovered.append(scenario_id)
        else:
            print(f"✓ {scenario_id}: Tests found ({len(test_files)} file(s))")

            # Run tests
            test_result = run_tests_for_marker(marker)

            if test_result['returncode'] == 0:
                print(f"   ✅ PASS ({test_result['passed']} test(s))")
                results.append((scenario_id, 'PASS', test_result['passed']))
            else:
                print(f"   ❌ FAIL ({test_result['failed']} failed)")
                failed_scenarios.append((scenario_id, test_result))
                results.append((scenario_id, 'FAIL', test_result['failed']))

        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    covered = len(scenarios) - len(uncovered)
    passed = sum(1 for _, status, _ in results if status == 'PASS')

    print(f"\nScenario Coverage: {covered}/{len(scenarios)} ({covered/len(scenarios)*100:.0f}%)")
    print(f"Test Results: {passed}/{covered} passing" if covered > 0 else "")

    if uncovered:
        print(f"\n⚠️  Uncovered Scenarios ({len(uncovered)}):")
        for scn_id in uncovered:
            print(f"   - {scn_id}: No tests with @pytest.mark.{scn_id.lower().replace('-', '')}")

    if failed_scenarios:
        print(f"\n❌ Failed Scenarios ({len(failed_scenarios)}):")
        for scn_id, result in failed_scenarios:
            print(f"   - {scn_id}: {result['failed']} test(s) failed")

    if covered == len(scenarios) and passed == covered:
        print("\n✅ All scenarios covered and passing!")
        sys.exit(0)
    else:
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_scenario_coverage.py <plan_file> [project_root]")
        print("Example: python check_scenario_coverage.py docs/plans/PLN-001-2025-10-26-report.md")
        sys.exit(1)

    plan_file = Path(sys.argv[1])

    # Get project root from argument or use current directory
    if len(sys.argv) > 2:
        project_root = Path(sys.argv[2]).resolve()
    else:
        project_root = Path.cwd()

    try:
        check_coverage(plan_file, project_root)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
