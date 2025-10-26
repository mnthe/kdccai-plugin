---
plan_id: {{PLAN_ID}}
status: pending
created: {{DATE}}
updated: {{DATE}}
language: python
author: {{USER_NAME}}
verified: false
verification_date: null
blocked_reason: null
---

# {{PLAN_NAME}}

## Requirements

### What to Build

[Describe what you want to build in user's own words]

### Why

[Explain the problem this solves or the goal it achieves]

### Success Criteria

[How will you know it works? What does "done" look like?]

## Scenarios

> Scenarios are concrete examples of how the tool will be used.
> Each scenario should be specific enough to test.

### SCN-001: [Scenario Name]

**Description**: [What happens in this scenario - be specific]

**Input**: [What data/files are needed? Give concrete examples]

**Expected Output**: [What should the result be? Be specific]

**Steps**:
1. [User action or system behavior]
2. [User action or system behavior]
3. [User action or system behavior]

### SCN-002: [Add more scenarios as needed]

[Repeat the pattern above for each scenario]

## Tasks

> Tasks are implementation steps derived from scenarios.
> Each task should contribute to one or more scenarios.

### Task 1: [Task Name]

**Related Scenarios**: SCN-001

**Description**: [What needs to be implemented to support the scenario]

**Acceptance Criteria**:
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

**Implementation Notes**:
[Any technical details, libraries to use, or approaches to consider]

**AI Note**:
Implement using TDD:
- Write test for each validation criterion
- Cover scenarios: [List related SCN-XXX]
- Tag tests with @pytest.mark.scnXXX

### Task 2: [Task Name]

**Related Scenarios**: SCN-001, SCN-002

**Description**: [What needs to be implemented]

**Acceptance Criteria**:
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]

**Implementation Notes**:
[Any technical details]

**AI Note**:
Implement using TDD:
- Write test for each validation criterion
- Cover scenarios: [List related SCN-XXX]
- Tag tests with @pytest.mark.scnXXX

## Verification

> How will we verify each scenario works as expected?

### SCN-001 Verification

**Command to run**:
```bash
[Command to execute the scenario, e.g., python src/report_generator.py]
```

**Expected result**:
[What should happen - be specific about files created, output shown, etc.]

### SCN-002 Verification

[Repeat for each scenario]

## Notes

[Any additional notes, constraints, assumptions, or future considerations]

**Constraints**:
- [Time, resource, or technical constraints]

**Assumptions**:
- [What are we assuming about the environment, data, or usage?]

**Future Extensions**:
- [Features that might be added later but are out of scope now]
