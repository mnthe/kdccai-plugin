# Non-Developer Skill System - Final Design (v3.0)

**Created**: 2025-10-26
**Updated**: 2025-10-26 (v3.0 - Python-only decision)
**Status**: Ready for Phase 1 Implementation
**Context**: 3-month AI Hackathon Pilot Program
**Target**: Non-developers (beginners ~ script users) building real work automation tools

---

## Executive Summary

A 4-skill system enabling non-developers to build real work automation tools through AI-assisted vibe coding, with hands-on support and Slack async help.

**Core Philosophy:**
- **Documentation = Source of Truth**: Code is black box, knowledge lives in docs
- **Phased Approach**: Month 1 (hands-on focused) → Month 2-3 (feedback-driven automation)
- **Language Strategy**: **Python-only Month 1** (TypeScript deferred to Month 2 based on demand)
- **Support Structure**: Biweekly meetings + Slack async support
- **Metadata-Driven**: Plan IDs, Scenario IDs for traceability

**Key Improvements from v2.0:**
- ✅ **Python-only Month 1**: Minimizes facilitator burden, maximizes focus
- ✅ Environment setup simplified (guide + hands-on, no devContainer)
- ✅ AI makes technical decisions (users only see business trade-offs)
- ✅ TDD completely hidden (users see Features + Validation Criteria)
- ✅ Slack sharing via copy-paste (MCP deferred to Phase 2)
- ✅ Hybrid phased rollout (basic → advanced)

---

## Program Context

### Timeline
- **Duration**: 3 months
- **Meetings**: Every 2 weeks (hands-on sessions)
- **Work Mode**: Async (participants use work hours)
- **Support**: Slack for async questions

### Participants
- **Background**: Mixed (complete beginners ~ script users)
- **Goal**: Build real work automation tools (not just demos)
- **Mindset**: Lower barrier to AI coding

### Success Metrics
- Participants complete real automation tools
- AI coding barrier significantly lowered
- **Secondary**: Pain point discovery, support method validation

---

## System Architecture

### Skill Structure (Phase 1 - Month 1)

```
0. project-init
   - Python-only setup (no language selection)
   - Setup guide (not automated)
   - CLAUDE.md + docs structure
   - Plan ID system initialization

1. plan
   - AI makes technical decisions
   - Metadata: Plan ID, Scenario IDs
   - TDD hidden (Feature + Validation Criteria)
   - Complexity assessment

2. implement
   - pytest-based TDD (internal execution)
   - Real-time progress display
   - Basic scenario coverage check
   - Auto-call debug on 3 failures

3. debug
   - 3 categories (A: Simple, B: Plan, D: Blocked)
   - Slack copy-paste sharing
   - User-friendly error translation
   - State save + resume
```

### Documentation Structure

```
project-root/
├── .claude/
│   └── CLAUDE.md              # Project context + language constraint
├── docs/
│   ├── knowledge-base/
│   │   ├── SETUP.md          # OS-specific setup guide
│   │   └── [domain-docs]      # API docs, business logic
│   ├── plans/
│   │   └── PLN-XXX-YYYY-MM-DD-feature-name.md  # Plan files
│   └── architecture/
│       └── [component].md     # Implementation summaries
├── src/                       # Actual code
├── tests/                     # Tests (@pytest.mark.scenario tags)
└── requirements.txt          # Python deps (auto-generated)
```

### Plan File Naming Convention

**Format:** `PLN-XXX-YYYY-MM-DD-feature-name.md`

**Examples:**
- `PLN-001-2025-10-26-excel-merger.md`
- `PLN-002-2025-10-27-web-scraper.md`

**Plan ID Generation:**
```python
# Auto-generated in plan skill
existing = glob("docs/plans/PLN-*.md")
max_id = max([int(f.split("-")[1]) for f in existing]) if existing else 0
new_id = f"PLN-{max_id + 1:03d}"
```

---

## Skill 0: project-init

### Purpose
Initialize project structure and provide setup guidance

### Phase 1 Characteristics
- Minimal automation (guide-focused)
- Assumes hands-on/Slack support
- **Language: Python-only** (Month 1 constraint)

### Execution Flow

**Step 0: Git Validation**
- Check git repo (flexible, allow brownfield)
- If CLAUDE.md exists → offer re-initialization

**Step 1: Explain Language Decision**
AI explains (in user's preferred language from context):
```
"This program uses Python in Month 1.
Python is powerful for data processing and automation, and easy to install.

If you need n8n or TypeScript:
- TypeScript support will be added in Month 2
- You can learn concepts with Python in Month 1, then apply in Month 2

Would you like to continue?"
```

**Step 2: Setup Guide (Not Automated)**
Generate SETUP.md in user's preferred language:
```
"Python installation is needed.
Setup guide saved to: docs/knowledge-base/SETUP.md

If you get stuck:
- Take screenshots
- Share error messages in Slack

After installation, run: python --version
Let me know the result to proceed."
```

**Step 3: User Context Collection**
- Preferred language (Korean, English, etc.)
- Work domain & tool purpose
- Technical background (beginner ~ script user)

**Step 4: Generate CLAUDE.md**
Auto-generate with:
- User context
- Selected language constraint
- Documentation = Source of Truth principle
- Plan ID system explanation

**Step 5: Create Documentation Structure**
```bash
mkdir -p docs/knowledge-base docs/plans docs/architecture
```

Generate SETUP.md with OS-specific installation guides

**Step 6: Git Commit**
```
git add .claude/ docs/
git commit -m "init: setup project for [domain]"
```

---

## Skill 1: plan

### Purpose
Decompose requirements into detailed implementation plan (non-dev friendly)

### Phase 1 Characteristics
- AI makes technical decisions
- Metadata auto-generation
- TDD completely hidden

### Guard Conditions
- Check CLAUDE.md exists
- If not → "Need project initialization first. Run project-init?"

### Execution Flow

**Phase 1: Understand Requirements (Brainstorming)**
- Ask questions one at a time
- Reference CLAUDE.md work domain
- Gather: Purpose, constraints, success criteria

**Phase 2: AI Auto-Select Approach (No User Choice)**
AI internal evaluation:
- CLAUDE.md technical background (beginner → simple approach)
- Requirements complexity
- Selected language (Python → pandas/openpyxl)

AI decides, then explains in **business language**:
```
"I'll use a powerful library for fast processing of large files.
Trade-off: 30-second installation on first run.
After that, it runs instantly. Is that okay?"
```

User confirms business trade-off:
- Installation time vs performance
- Simplicity vs feature richness
- File count limits

**Phase 3: Scenario Definition (Golden Path Prevention)**
AI judges context:
- Special case only? vs General-purpose needed?
- Confirm with user

Define 3-5 scenarios:
- Scenario 1 (Happy path): Normal case
- Scenarios 2-4 (Edge cases): Empty files, large volume, invalid format
- Auto-assign IDs: SCN-001, SCN-002, ...

**Phase 4: Write Plan Document (User-Friendly Structure)**

File: `docs/plans/PLN-XXX-YYYY-MM-DD-feature-name.md`

```markdown
---
plan_id: PLN-001
status: pending
created: 2025-10-26
updated: 2025-10-26
language: python
author: user_name
verified: false
verification_date: null
blocked_reason: null
---

# [Feature Name] Implementation Plan

**Goal:** [One sentence description]

**How it works:**
[2-3 sentences understandable by non-developers]

**Requirements:**
- Installation: pandas library (auto-installed)
- Estimated time: ~60 minutes

**Scenarios:**
- SCN-001: Merge 3 normal files
- SCN-002: Handle empty files (warning + skip)
- SCN-003: Process 100+ files (no memory issues)
- SCN-004: Detect column mismatch (clear error)

---

## Task 1: File Reading Feature

**Feature:**
Read multiple Excel files and combine them into one.

**Validation Criteria:**
- [ ] Can read 3 files successfully
- [ ] Empty files trigger warning and get skipped
- [ ] Can process 100+ files without memory issues
- [ ] Column structure mismatch shows clear error

**Related Files:**
- src/merger.py - Merge logic
- tests/test_merger.py - Validation tests

**AI Note:**
Implement using TDD:
- Write test for each validation criterion
- Cover scenarios SCN-001, SCN-002, SCN-003, SCN-004
- Tag with @pytest.mark.scenario("SCN-XXX")

## Task 2: [Next Task]
...
```

**Phase 5: Complexity Assessment**
Calculate:
- Total tasks: 5
- Estimated time: 60 minutes
- Dependencies: pandas (Medium)
- Scenarios: 4

Present to user:
```
"This plan has 5 tasks, estimated ~60 minutes.
Complexity: Medium

Is this okay? Or should we simplify?"

Options:
- "Proceed" → Move to implement
- "Simplify (happy path only)" → Remove edge case scenarios
- "Break into phases" → Split into multiple smaller plans
```

**Phase 6: Git Commit**
```
git add docs/plans/PLN-001-2025-10-26-excel-merger.md
git commit -m "plan(PLN-001): add implementation plan for excel merger"
```

---

## Skill 2: implement

### Purpose
Execute Plan to generate code, tests, validation (TDD internal)

### Phase 1 Characteristics
- TDD completely hidden
- Real-time progress display only
- Basic scenario coverage check (no blocking)
- Auto-call debug on failures

### Guard Conditions
1. Check CLAUDE.md exists → If not, suggest project-init
2. Check docs/plans/ for `status: pending` or `in-progress` plan
   → If none, suggest plan skill

### Execution Flow

**Step 1: Load Plan & Create TodoWrite**
- Read plan file (PLN-XXX)
- Register all Tasks to TodoWrite
- Display to user:
  ```
  "Starting 5 tasks.
   Progress will be shown in real-time."
  ```

**Step 2: TDD-based Implementation (Internal, Hidden from User)**

For each Task:

  **Display to user:**
  ```
  [In Progress] Task 1/5: File Reading Feature
  ```

  **AI internal (TDD):**
  1. Write test for criterion 1 → Run (FAIL) → Implement → Run (PASS)
  2. Write test for criterion 2 → ...
  3. ...

  **Progress display:**
  ```
    ✓ Validation: Read 3 files successfully
    [In Progress] Validation: Handle empty files...
  ```

  **Failure handling:**
  - Same test fails 3 times consecutively → Auto-call debug skill
  - Debug result → Recover or escalate to user

  **Success:**
  - Git commit (automatic)
  - TodoWrite mark completed
  - Display: "✓ Task 1 completed (5 minutes)"

**Step 3: Basic Validation (Phase 1 Simplified)**

After all Tasks complete:

**Scenario Coverage Basic Check:**
```python
for scenario in plan.scenarios:
    tests = find_tests_with_tag(f"@pytest.mark.scenario('{scenario.id}')")
    if len(tests) == 0:
        WARN(f"No test for scenario {scenario.id}")
        # Phase 1: Warning only, don't block
    else:
        result = run_tests(tests)
        display(f"✓ {scenario.name}: {result}")
```

**Display to user:**
```
Automated validation results:
 ✓ SCN-001: Normal file merge - PASS
 ✓ SCN-002: Empty file handling - PASS
 ✓ SCN-003: Large volume processing - PASS
 ⚠ SCN-004: Invalid format - No test

Warning: Scenario 4 not validated.
Add test now, or later?
```

**Step 4: Update Plan Status**
- Change plan status to `completed`
- Add simple implementation summary to docs/architecture/:

  ```markdown
  # merger.py

  **Function:** Merge multiple Excel files into one

  **Input:** Excel files (.xlsx)
  **Output:** Single merged Excel file

  **How it works:**
  - Uses pandas library
  - Auto-skips empty files
  - Errors on column structure mismatch
  ```

**Step 5: User Verification (Manual)**
AI actually runs the tool:
```
"Now I'll run it to verify.

Command: python src/merger.py sample_data/*.xlsx

Output:
  Processing complete: 3 files merged → output.xlsx
  - sample1.xlsx: 50 rows
  - sample2.xlsx: 30 rows
  - sample3.xlsx: 20 rows
  Total: 100 rows

Result file created: output.xlsx
Open it and check: Does it have 100 rows as expected?"
```

User responds:
- "Yes, correct" → Complete
- "No, something's wrong" → Call debug skill
- "Don't know how to check" →
  ```
  "Open output.xlsx in Excel.
   Look at bottom status bar: should show '100 rows'."
  ```

**Step 6: Record Verification & Git Commit**
Add to plan file:
```yaml
---
status: completed
verified: true
verification_date: 2025-10-26
verification_method: user_manual
---
```

Commit all changes:
```bash
git add src/ tests/ docs/
git commit -m "feat(PLN-001): implement excel merger with tests"
```

**Step 7: Completion Message**
```
Implementation complete! 🎉

Your tool:
- src/merger.py: Main program
- Run: python src/merger.py [files]

Next steps:
- Test with your real work files
- Report any issues anytime
- Add new features with a new plan

[Show Example] [Copy Slack Message] [Add Feature]
```

---

## Skill 3: debug

### Purpose
Analyze and recover from implementation failures (Phase 1 basic version)

### Phase 1 Characteristics
- 3 categories only (A, B, D)
- Category E (Pivot) deferred to Month 2
- Slack sharing via copy-paste
- User-friendly error translation

### Trigger Conditions
1. implement skill: 3 consecutive failures
2. User explicit: "There's a problem"
3. User manual verification: "No, something's wrong"

### Execution Flow

**Step 1: Collect Context**
Auto-collect:
- Error message
- Failing test code
- Related implementation code
- Current Plan
- Recent Git commit history

Display to user:
```
"Analyzing the problem...
[Analyzing: Error message]
[Analyzing: Code review]"
```

**Step 2: Classify Problem (3-Category)**

AI internal classification:
- Error type analysis
- Failure count and pattern
- Compare Plan vs implementation

**Category A: Simple Bug** (AI can fix)
- Example: Typo, missing import, simple logic error
- Criteria: Error is clear, 1-2 line fix

**Category B: Plan Flaw** (Plan issue)
- Example: Plan asks for impossible thing, requirements vague
- Criteria: Error repeats, Plan assumption wrong

**Category D: Blocked** (Unsolvable)
- Example: External API down, no permissions, environment issue
- Criteria: Tried 3 different approaches, all failed

**Category C (Environment)** excluded in Phase 1:
→ Environment issues resolved via hands-on/Slack

**Step 3: Category-Specific Actions**

**=== Category A: Simple Bug ===**
Display to user:
```
"Found a simple error.
Fixing..."
```

AI action:
- Fix code
- Re-run tests
- Success → Resume implement
- Failure → Re-classify (→ B or D)

Display:
```
"✓ Fixed! Continuing..."
```

**=== Category B: Plan Flaw ===**
Display to user (plain language):
```
"Found an issue in the plan.

**Problem:**
The plan said 'auto-detect all date formats', but
date formats are too varied for auto-detection.

**Cause:**
CSV files have dates in different formats:
'2024-01-01', 'Jan 1, 2024', '01/01/24', etc.

**Solutions:**
1. Simplify: Support only common format (YYYY-MM-DD)
2. User input: Ask user for date format when running
3. Pre-process: Build a tool to unify date formats first

What would you like to do?"
```

User selects → Go to plan skill to revise Plan → Resume implement

**=== Category D: Blocked ===**
Display to user:
```
"I'm sorry, I can't solve this problem.

**What I tried:**
1. Different library (openpyxl → xlrd)
2. Changed file reading method
3. Ignore errors and continue

**Problem:**
File is password-protected and cannot be read.

**What's needed:**
- File password required
- Or password-free version of file needed

Need help? Share in Slack.
[Copy for Slack]"
```

**Step 4: Slack Sharing (Copy-Paste)**

User clicks [Copy for Slack]:

Auto-generate message → **Copy to clipboard** + Display:

```
┌─────────────────────────────────────────────┐
│ 📋 Copied to clipboard                      │
│ Paste (Ctrl+V / Cmd+V) in Slack            │
└─────────────────────────────────────────────┘

=== Copied Content ===

🆘 Help Request

**Project:** Excel File Merger
**Problem:** Cannot read password-protected file

**Error Message:**
```
xlrd.biffh.XLRDError: Workbook is encrypted
```

**What I tried:**
1. openpyxl library → Same error
2. xlrd library → Same error
3. Skip file option → Missing required data

**Environment:**
- OS: macOS 14.0
- Python: 3.11.5
- Libraries: pandas 2.1.0, openpyxl 3.1.0

**File Location:**
- Plan: docs/plans/PLN-001-2025-10-26-excel-merger.md
- Code: src/merger.py (line 45)

====================

User guide:
"Go to Slack and paste this message.
Add screenshots if needed.

If paste didn't work, copy the text above manually."

[Re-copy] [Open Slack] [Continue]
```

**Step 5: Save State**
Update plan file:
```yaml
---
status: blocked
blocked_reason: "Encrypted file - need password"
blocked_date: 2025-10-26
debug_category: D
---
```

Git commit:
```bash
git commit -m "debug(PLN-001): blocked on encrypted file issue"
```

**Step 6: User Guidance**
```
"Current state saved.
You can restart anytime after resolving the issue.

After resolution:
1. Remove password from file or get new file
2. Run implement skill again
3. Automatically resumes from where it stopped"
```

---

## State Management & Resumption

### State Tracking Methods

1. **Plan file status metadata**
2. **Git commit history**
3. **TodoWrite** (in-session progress)

### Git Commit Conventions

```bash
# project-init
"init: setup project for [domain]"

# plan
"plan(PLN-001): add feature plan for [feature]"

# implement
"feat(PLN-001): implement task 1/5 - [task name]"
"test(PLN-001): add tests for SCN-002"

# debug
"debug(PLN-001): fix [category A/B/D] issue"
"debug(PLN-001): blocked - [reason]"
```

### Resumption Flow

When user returns:
1. Check Git log → Identify last work
2. Check Plan file status
3. Display: "Last time you completed [work]. Continue?"

---

## Phase 2 Features (Month 2-3)

Deferred to Month 2 based on Month 1 feedback:

### 1. TypeScript Support (Demand-Based)
- Build Vitest/Jest test harness with scenario tagging
- Create TypeScript SETUP.md templates
- Update project-init for language selection
- Enable n8n workflow automation use cases

### 2. Project Dashboard
- Current status visualization
- List of completed/in-progress/pending Plans
- Slack integration status

### 3. debug - Category E (Pivot)
- Suggest completely different approach
- Propose intermediate tool creation
- Example: "CSV parsing too hard → Build CSV-to-Excel converter first"

### 4. Enhanced Auto-Enforcement
- Block commits if scenario has no test
- Coverage gating (80% requirement)
- Automated doc-code verification

### 5. Slack MCP Integration
- Auto-send messages
- Thread-based conversations
- Notification settings

### 6. Environment Auto-Fix
- Category C in debug skill
- Auto-detect environment issues
- Guided environment repair

---

## Implementation Priorities

### Month 1 (Phase 1 - Critical)
**Week 1-2:**
1. Implement project-init skill
2. Implement plan skill
3. Create SETUP.md templates

**Week 3-4:**
1. Implement implement skill (basic)
2. Implement debug skill (3-category)
3. Integration testing

**Hands-on Session 1:**
- Environment setup support
- First project initialization
- Pain point collection

### Month 2 (Phase 2 - Feedback-Driven)
**Week 5-6:**
- Analyze Month 1 pain points
- **Evaluate TypeScript demand** (survey participants)
- Prioritize automation features
- Implement top 3 pain point solutions

**Week 7-8:**
- **Add TypeScript support if demand ≥20%** (Vitest harness)
- Add Category E to debug
- Enhance scenario enforcement
- Dashboard prototype

**Hands-on Session 2:**
- Review automation improvements
- Advanced feature walkthrough
- TypeScript introduction (if added)

### Month 3 (Phase 3 - Polish)
**Week 9-10:**
- Slack MCP integration
- Coverage gating
- Documentation polish

**Week 11-12:**
- Final testing
- Participant showcase preparation
- Retrospective & feedback collection

---

## Success Criteria

### Quantitative
- 80%+ participants complete at least 1 working tool
- 50%+ participants complete 2+ tools
- Average Slack response time < 4 hours

### Qualitative
- Participants report "AI coding feels approachable"
- Participants can explain their tool to colleagues
- Participants want to continue using skills post-program

### Learning Metrics (for iteration)
- Top 5 most common pain points identified
- Most effective support methods identified
- Most requested features for Phase 2

---

## Key Design Decisions Summary

### From Original Design
✅ **Kept:**
- Documentation = Source of Truth philosophy
- 3-skill architecture (init, plan, implement)
- Guard pattern with auto-execution
- TDD workflow (but hidden from user)

❌ **Changed:**
- devContainer → Simple setup guide + hands-on
- Automated environment setup → Manual with support
- User selects library → AI auto-selects, explains business value
- Exposed TDD steps → Hidden, show Features + Validation only
- Slack MCP → Copy-paste (MCP in Phase 2)

### From Codex Feedback
✅ **Implemented:**
- Metadata system (Plan ID, Scenario ID)
- Pytest marker tags for scenario mapping
- **Python-only Month 1** (minimizes complexity)
- State storage in Plan files + Git

⏭️ **Deferred to Phase 2:**
- TypeScript support (based on demand)
- Cross-language projects
- Database/service dependencies
- Credential management
- Advanced enforcement (coverage gating)

### From Gemini Feedback
✅ **Implemented:**
- AI makes technical decisions
- Business language explanations
- TDD completely hidden
- User verification with specific guidance
- Slack copy-paste sharing

⏭️ **Deferred to Phase 2:**
- Category E (Pivot)
- Project Dashboard
- Cloud environment option
- Version history UI

### From v3.0 Language Decision (Python-only Month 1)

**Decision Rationale:**
1. **Facilitator burden minimization**: Single tech stack reduces support complexity
2. **Clear focus**: Data automation primary use case (70-80% coverage estimate)
3. **Month 1 is learning phase**: Full coverage unnecessary, pain point discovery is primary goal
4. **TypeScript deferred, not abandoned**: Month 2 expansion based on actual demand signals

**Alternative Approaches Considered:**
- **Option A (Python-only)**: ✅ Selected - Clear scope, minimal complexity
- **Option B (Both Python + TypeScript)**: Rejected - 6-8hr harness build, 2x support burden
- **Option C (Survey-driven)**: Partial adoption - Will survey in Month 2 for demand validation

**External Validation:**
- **Codex**: Recommended survey + parallel Vitest skeleton prep
- **Gemini**: Recommended "Survey → Support Both" for inclusion
- **Final Decision**: Month 1 focus > early inclusion, data-driven Month 2 expansion

**Risk Mitigation:**
- Clear communication: "Month 1 = Python, Month 2 = TypeScript if demand"
- Alternative paths for n8n users: Skip Month 1 or learn concepts with Python
- Demand threshold: TypeScript added if ≥20% participants request

---

## Next Steps

1. ✅ Design complete and validated (v3.0)
2. ⏭️ Write 4 skill files (project-init.md, plan.md, implement.md, debug.md)
3. ⏭️ Create Python SETUP.md templates (Windows, macOS, Linux)
4. ⏭️ Test with pilot user (dry run)
5. ⏭️ Iterate based on pilot feedback
6. ⏭️ Launch Month 1 with first cohort

---

## Appendix: File Templates

### CLAUDE.md Template

```markdown
# Project Context for AI

## User Context

### Preferred Language
ko-KR

### Work Domain & Purpose
Marketing team - merge monthly sales reports from multiple branches

### Technical Background
Beginner - can run simple Python scripts

### Project Type
CLI tool - local execution

---

## Language Constraint

**Month 1:** Python only
**Month 2+:** TypeScript support based on participant demand

**Selected:** Python
**Reason:**
- Best for data processing and automation (primary use case)
- Minimizes facilitator burden (single tech stack)
- Month 1 focus: Learn pain points with clear scope

---

## Core Operating Principles

### Documentation = Source of Truth
- All knowledge lives in docs
- Code is black box implementation
- Changes reflected in docs first or simultaneously

### Documentation Structure
- `docs/knowledge-base/`: Domain knowledge, setup guides
- `docs/plans/`: Implementation plans (PLN-XXX-YYYY-MM-DD-name.md)
- `docs/architecture/`: Component descriptions

### Plan ID System
- Format: PLN-001, PLN-002, ...
- Auto-incremented
- Included in file names for easy reference

### Validation Strategy
- Automated tests (TDD, hidden from user)
- Manual verification with executable commands
- Scenario coverage tracking

### Development Workflow
1. Plan (requirements → scenarios → tasks)
2. Implement (TDD internal, progress visible)
3. Verify (auto + manual)
4. Git commit

### Communication Language
All communication with user must be in: Korean
```

### Plan File Template

```markdown
---
plan_id: PLN-001
status: pending
created: 2025-10-26
updated: 2025-10-26
language: python
author: user_name
verified: false
verification_date: null
blocked_reason: null
---

# [Feature Name] Implementation Plan

**Goal:** [One sentence]

**How it works:**
[2-3 sentences for non-developers]

**Requirements:**
- Installation: [libraries]
- Estimated time: ~XX minutes

**Scenarios:**
- SCN-001: [Happy path description]
- SCN-002: [Edge case 1]
- SCN-003: [Edge case 2]

---

## Task 1: [Task Name]

**Feature:**
[Plain language description]

**Validation Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Related Files:**
- src/[file].py
- tests/test_[file].py

**AI Note:**
Implement with TDD, tag tests with @pytest.mark.scenario("SCN-XXX")
```

---

**End of Design Document**
