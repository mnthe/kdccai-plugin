---
name: implement
description: Use when user wants to implement tasks from a plan (PLN-XXX). Uses TDD internally (hidden from user), guides through task-by-task implementation with progress updates in user's preferred language. Triggered by "/implement" command or requests like "구현하고 싶어요" or "코드 작성해주세요".
---

# Implement

## Overview

This skill implements tasks from plan documents (PLN-XXX) using Test-Driven Development (TDD) internally while showing clean progress updates to the user.

**Use this skill when:**
- User wants to implement a plan
- User says "/implement" or "구현하고 싶어요"
- User completed planning and is ready to code
- User asks to implement specific tasks from a plan

**Output**: Working code in `src/`, tests in `tests/`, updated plan document

---

## Workflow

### Step 1: Load Context

**Goal**: Understand user's background and the plan to implement.

**Process**:

1. **Read CLAUDE.md** from project root:
   ```
   Read: CLAUDE.md
   ```

2. **Extract**:
   - Preferred communication language
   - Work domain
   - Technical background

3. **Find plan** to implement:
   - If user specified: "PLN-001을 구현하고 싶어요"
   - If not specified, list available plans:
     ```bash
     ls docs/plans/
     ```
   - Ask user which plan to implement

4. **Read plan document**:
   ```
   Read: docs/plans/PLN-XXX-YYYY-MM-DD-name.md
   ```

5. **Extract from plan**:
   - Requirements
   - Scenarios
   - Tasks (with acceptance criteria)
   - Verification commands

---

### Step 2: Set Up Environment

**Goal**: Ensure project structure and dependencies are ready.

**Process**:

1. **Check project structure exists**:
   ```bash
   ls src/ tests/
   ```

   If missing:
   ```bash
   mkdir -p src tests
   ```

2. **Check for virtual environment**:
   ```bash
   ls venv/
   ```

   If not exist, remind user:
   - Korean: "먼저 가상 환경을 만들어주세요: `python -m venv venv` 그리고 활성화: `source venv/bin/activate`"
   - English: "Please create a virtual environment first: `python -m venv venv` and activate it: `source venv/bin/activate`"

---

### Step 3: Choose Implementation Order

**Goal**: Determine which tasks to implement and in what order.

**Process**:

1. **Show task list** to user:
   ```
   이 계획에는 3개 태스크가 있습니다:
   - Task 1: Facebook API 연동 [미완료]
   - Task 2: Instagram API 연동 [미완료]
   - Task 3: Excel 리포트 생성 [미완료]

   어떤 순서로 구현할까요?
   1. 순서대로 전부 구현 (Task 1 → 2 → 3)
   2. 특정 태스크만 구현
   ```

2. **Get user's choice**

3. **Create implementation checklist** with TodoWrite:
   - One todo per task
   - Mark as pending initially

---

### Step 4: Implement Each Task (TDD Cycle)

**Goal**: Implement one task at a time using TDD (hidden from user).

**For each task, repeat**:

#### 4.1. Announce Task Start

```
AI: Task 1 시작: Facebook API 연동
    페이스북에서 좋아요, 댓글, 공유 수를 가져오는 기능을 만들겠습니다.
```

Update TodoWrite: Mark task as in_progress

---

#### 4.2. TDD Cycle (Internal - Hidden from User)

**Read TDD guide**:
```
Read: references/tdd-guide.md
```

**Process (internal)**:

1. **Write test first** in `tests/test_<module>.py`
   - Use pytest
   - Add `@pytest.mark.scnXXX` marker to map to scenarios
   - Cover acceptance criteria from plan

2. **Run test → RED** (should fail)
   ```bash
   pytest tests/test_<module>.py -v
   ```

3. **Implement minimal code** in `src/<module>.py`
   - Read common patterns:
     ```
     Read: references/common-patterns.md
     ```
   - Read library recommendations:
     ```
     Read: references/library-recommendations.md
     ```
   - Write clean, simple code

4. **Run test → GREEN** (should pass)
   ```bash
   pytest tests/test_<module>.py -v
   ```

   **If test fails 3 consecutive times** (same test, same error):
   - Auto-trigger debug skill:
     ```
     Skill: debug
     ```
   - Provide debug context: error message, test code, implementation code
   - Wait for debug result
   - If debug fixes issue → Continue with GREEN
   - If debug escalates → Inform user, wait for guidance

5. **Refactor if needed**
   - Clean up code
   - Add error handling
   - Add logging

**DO NOT show test code to user** - only show implementation code when asked.

---

#### 4.3. Show Progress to User

**After test passes**:

```
AI: Task 1 완료 ✅
    src/facebook_client.py를 생성했습니다.
    페이스북 API에 연결하고 engagement 데이터를 가져올 수 있습니다.

    사용 방법:
    ```python
    from src.facebook_client import FacebookClient

    client = FacebookClient(api_key="...")
    data = client.fetch_engagement(page_id="우리회사")
    print(data)  # {'likes': 100, 'comments': 20, 'shares': 5}
    ```
```

Update TodoWrite: Mark task as completed

---

#### 4.4. Mark Task in Plan Document

```bash
python scripts/mark_task_done.py docs/plans/PLN-XXX-... 1
```

This checks all acceptance criteria checkboxes for Task 1.

---

#### 4.5. Handle Dependencies

**If task requires dependencies**:

1. **Inform user**:
   ```
   이 태스크는 facebook-sdk 라이브러리가 필요합니다.
   설치하시겠어요? `pip install facebook-sdk`
   ```

2. **Wait for user confirmation**

3. **Update requirements.txt**:
   ```
   # If requirements.txt doesn't exist, create it
   # Add new dependency with version
   facebook-sdk==3.1.0
   ```

---

### Step 5: Integration and End-to-End Test

**Goal**: Verify all tasks work together for each scenario.

**Process**:

1. **After all tasks for a scenario are complete**, create main script:
   ```python
   # src/report_generator.py
   from facebook_client import FacebookClient
   from instagram_client import InstagramClient
   from excel_generator import generate_excel

   def main():
       # Integrate all components
       pass

   if __name__ == '__main__':
       main()
   ```

2. **Check scenario coverage** (automated):
   ```bash
   python scripts/check_scenario_coverage.py docs/plans/PLN-XXX-...
   ```

   **This checks**:
   - All scenarios in plan have tests with @pytest.mark.scnXXX
   - Runs tests for each scenario
   - Reports coverage and results

   **Output example**:
   ```
   Found 3 scenario(s): SCN-001, SCN-002, SCN-003

   ✓ SCN-001: Tests found (2 file(s))
      ✅ PASS (5 test(s))

   ✓ SCN-002: Tests found (1 file(s))
      ✅ PASS (2 test(s))

   ⚠️  SCN-003: No tests found

   Summary:
   Scenario Coverage: 2/3 (67%)
   Test Results: 2/2 passing
   ```

   **If any scenario uncovered**:
   - **Phase 1**: Show warning, don't block
   - Ask user: "SCN-003에 테스트가 없습니다. 지금 추가할까요, 나중에 할까요?"
   - User can choose to add now or defer

3. **Run scenario verification** from plan document:
   ```bash
   python src/report_generator.py
   ```

4. **Check expected output**:
   - File created?
   - Correct content?
   - Matches scenario expectations?

5. **If verification passes**:
   ```
   AI: SCN-001 검증 완료 ✅
       reports/engagement-2025-10-26.xlsx 파일이 생성되었습니다.
       시나리오에 정의된 대로 작동합니다!
   ```

6. **If verification fails** → Use debug skill

7. **Update plan status to completed**:
   ```bash
   python scripts/update_plan_status.py docs/plans/PLN-XXX-... completed
   ```

   This updates the plan's YAML frontmatter:
   - status: completed
   - verified: true
   - verification_date: YYYY-MM-DD
   - updated: YYYY-MM-DD

---

### Step 6: Documentation Update

**Goal**: Update docs/architecture/ with how the implementation works.

**Process**:

1. **Create architecture document**:
   ```
   Write: docs/architecture/PLN-XXX-implementation.md
   ```

2. **Document structure**:
   ```markdown
   # PLN-XXX Implementation

   ## Overview
   [Brief description of what was built]

   ## Components

   ### src/facebook_client.py
   - Purpose: Connect to Facebook API and fetch engagement data
   - Key functions:
     - `fetch_engagement(page_id)`: Returns dict with likes, comments, shares

   ### src/excel_generator.py
   - Purpose: Generate Excel report from engagement data
   - Key functions:
     - `generate_excel(data, output_path)`: Creates formatted Excel file

   ## Dependencies
   - facebook-sdk==3.1.0
   - openpyxl==3.1.2

   ## Usage
   ```bash
   python src/report_generator.py
   ```

   ## How It Works
   1. Reads API credentials from .env
   2. Fetches data from Facebook and Instagram
   3. Calculates total engagement
   4. Generates Excel file with two sheets
   ```

3. **Inform user**:
   ```
   구현 문서를 작성했습니다: docs/architecture/PLN-001-implementation.md
   나중에 참고할 수 있도록 작동 방식을 기록했습니다.
   ```

---

### Step 7: Git Commit

**Goal**: Create commit referencing the plan ID.

**Process**:

1. **Show changes**:
   ```bash
   git status
   git diff
   ```

2. **Ask user if ready to commit**:
   ```
   변경사항을 커밋할까요?
   - src/ 폴더에 새 파일 추가
   - tests/ 폴더에 테스트 추가
   - docs/plans/PLN-001-... 업데이트 (태스크 완료 체크)
   - docs/architecture/PLN-001-implementation.md 추가
   ```

3. **If user agrees**:
   ```bash
   git add src/ tests/ docs/
   git commit -m "Implement Tasks 1-3 from PLN-001

   - Add Facebook API client
   - Add Instagram API client
   - Add Excel report generator
   - Complete SCN-001: Daily engagement report

   Ref: PLN-001"
   ```

---

### Step 8: Next Steps Guidance

**Goal**: Guide user on what to do next.

**Process**:

1. **If all tasks complete**:
   ```
   모든 태스크 구현 완료! ✅

   다음 단계:
   1. 실제 데이터로 테스트해보세요: `python src/report_generator.py`
   2. 문제가 생기면 [debug] 스킬 사용하기
   3. 새 기능 추가는 새 계획(PLN-002)을 먼저 작성하세요

   "/debug" 또는 "/plan"을 입력하세요.
   ```

2. **If partial completion**:
   ```
   Task 1-2 완료! ✅ (Task 3 남음)

   계속 구현할까요?
   1. 다음 태스크 구현 (Task 3)
   2. 여기서 중단하고 나중에 계속
   ```

---

## Key Principles

### TDD is Hidden from User

**DO**:
- Write tests first (internally)
- Run tests to verify (internally)
- Only show code to user when tests pass

**DON'T**:
- Show test code to user (unless they ask)
- Mention pytest in regular updates
- Explain testing process to user

**User sees**: "Task 1 완료 ✅"

**User doesn't see**: "Wrote test_facebook_client.py, ran pytest, all tests passed"

---

### Progressive Implementation

**One task at a time**:
- Complete Task 1 fully → Show user → Mark done
- Then Task 2 → Show user → Mark done
- Don't try to do everything at once

**Why**: Easier to debug, user can test incrementally

---

### Communication in User's Language

**Adapt technical depth** based on user's background (from CLAUDE.md):
- Non-technical: Simple explanations, avoid jargon
- Semi-technical: Use library names, show code examples
- Technical: Full technical details

**Example (non-technical)**:
```
페이스북에 연결하는 코드를 만들었습니다.
API 키를 .env 파일에 넣으면 데이터를 가져올 수 있어요.
```

**Example (semi-technical)**:
```
facebook-sdk 라이브러리를 사용해서 FacebookClient 클래스를 만들었습니다.
.env 파일의 FACEBOOK_API_KEY로 인증하고, fetch_engagement() 메서드로 데이터를 가져옵니다.
```

---

### Use Common Patterns

**Load references as needed**:
```
Read: references/common-patterns.md
```

Find patterns for:
- CSV/Excel file I/O
- API calls
- Date/time handling
- Error handling
- Logging

**Don't reinvent** - use proven patterns.

---

### Library Selection

**Load library recommendations**:
```
Read: references/library-recommendations.md
```

Based on domain (from CLAUDE.md):
- Marketing → requests, openpyxl, facebook-sdk, instagrapi
- Finance → pandas, openpyxl, pdfplumber
- Sales → requests, openpyxl
- HR → requests, openpyxl, PyYAML

**Prefer built-in libraries** when possible.

---

## Troubleshooting

### Tests Keep Failing

**Symptom**: Test fails after 2-3 attempts to fix

**Solution**:
1. **Review test expectations** - Are they realistic?
2. **Check implementation logic** - Is there a fundamental error?
3. **Simplify** - Break into smaller functions
4. **Ask for help** - External validation might reveal issue

**Inform user**:
```
Task 1을 구현하는 중 문제가 발생했습니다.
Facebook API 인증에서 오류가 나는데, API 키가 올바른지 확인해주시겠어요?
```

Be specific about what's needed.

---

### Missing Dependencies

**Symptom**: Import error when running code

**Solution**:
1. **Identify missing library**
2. **Install**: `pip install <library>`
3. **Add to requirements.txt**
4. **Re-run test**

**Inform user**:
```
openpyxl 라이브러리가 필요합니다.
설치할까요? `pip install openpyxl`
```

---

### User Wants to See Test Code

**Symptom**: "테스트 코드 보여주세요"

**Solution**:
```
AI: 테스트 코드는 tests/test_facebook_client.py에 있습니다.

    [Shows test code]

    pytest로 실행할 수 있습니다: `pytest tests/ -v`
```

**It's okay to show tests when asked** - just don't show them proactively.

---

### Task Dependencies Are Wrong

**Symptom**: Task 3 needs Task 1, but they're defined independently

**Solution**:
1. **Identify dependency**
2. **Implement in correct order** (Task 1 → Task 3)
3. **Update plan** if needed to clarify dependencies

---

## Resources

### scripts/
- `mark_task_done.py` - Mark task as completed in plan document (checks all acceptance criteria)
- `update_plan_status.py` - Update plan status in YAML frontmatter (pending → in_progress → completed)
- `check_scenario_coverage.py` - Check if all scenarios have tests with pytest markers, run tests per scenario

### references/
- `tdd-guide.md` - TDD workflow (hidden from user): RED → GREEN → REFACTOR cycle, testing patterns
- `common-patterns.md` - Ready-to-use code patterns for CSV, Excel, API, dates, logging, error handling
- `library-recommendations.md` - Domain-specific library recommendations (marketing, finance, sales, HR, data processing)

---

## Example Session

```
User: /implement

AI: [Loads CLAUDE.md and finds plans]

AI: 어떤 계획을 구현할까요?
    1. PLN-001-2025-10-26-social-media-report.md

User: PLN-001이요

AI: [Reads plan document]

    PLN-001에는 3개 태스크가 있습니다:
    - Task 1: Facebook API 연동
    - Task 2: Instagram API 연동
    - Task 3: Excel 리포트 생성

    순서대로 전부 구현할까요?

User: 네

AI: [Creates TodoWrite todos]

    좋습니다! Task 1부터 시작하겠습니다.

AI: [Internally: writes test, implements code, runs test → GREEN]

    Task 1 완료 ✅
    src/facebook_client.py를 생성했습니다.

    [Shows usage example]

AI: [Marks task done in plan]

AI: Task 2 시작: Instagram API 연동...

    [Repeats TDD cycle]

    Task 2 완료 ✅

AI: Task 3 시작: Excel 리포트 생성...

    openpyxl 라이브러리가 필요합니다.
    설치할까요? `pip install openpyxl`

User: 네

AI: [Installs, updates requirements.txt, implements Task 3]

    Task 3 완료 ✅

AI: 모든 태스크 완료! SCN-001 검증을 시작합니다...

    [Runs: python src/report_generator.py]

    ✅ reports/engagement-2025-10-26.xlsx 생성 완료!
    시나리오대로 작동합니다.

AI: [Creates architecture doc, commits]

    구현 완료! 변경사항을 커밋했습니다.

    다음 단계:
    1. 실제 데이터로 테스트: `python src/report_generator.py`
    2. 문제 발생 시: "/debug"
    3. 새 기능 추가: "/plan"
```
