---
name: plan
description: Use when user wants to create an implementation plan for their automation tool. Guides through requirements gathering → scenario definition → task breakdown. Creates PLN-XXX plan documents in docs/plans/. Triggered by "/plan" command or natural language requests like "계획 세우고 싶어요" or "무엇을 만들지 정리하고 싶어요".
---

# Plan

## Overview

This skill helps non-developers create structured implementation plans by transforming vague requirements into concrete, testable scenarios and tasks.

**Use this skill when:**
- User wants to create a new implementation plan
- User says "/plan" or "계획 세우고 싶어요"
- User completed project-init and is ready to plan what to build
- User asks "무엇을 만들지 정리하고 싶어요"

**Output**: Plan document in `docs/plans/PLN-XXX-YYYY-MM-DD-name.md`

## Workflow

### Step 1: Load User Context

**Goal**: Understand user's background and communication preferences.

**Process**:

1. **Read CLAUDE.md** from project root:
   ```
   Read: CLAUDE.md
   ```

2. **Extract key information**:
   - Preferred communication language
   - Work domain (marketing, finance, sales, etc.)
   - Technical background
   - Tool purpose

3. **Set communication language** for the rest of the session based on CLAUDE.md

**Why this matters**:
- Adjust technical depth based on user's background
- Use domain-relevant examples (see `references/scenario-examples.md`)
- Communicate in user's preferred language

---

### Step 2: Gather Requirements

**Goal**: Understand what the user wants to build and why.

**Process**:

1. **Ask about the goal** (in user's preferred language):
   - Korean: "무엇을 자동화하고 싶으신가요? 현재 어떤 작업을 하고 계시고, 어떤 부분이 불편하신가요?"
   - English: "What would you like to automate? What task are you currently doing manually?"

2. **Listen for**:
   - **What**: The task or process to automate
   - **Why**: The pain point or goal
   - **How often**: Daily? Weekly? On-demand?
   - **Current process**: How they do it now

3. **Probe for specifics**:
   - "구체적인 예를 들어주실 수 있나요?" / "Can you give a specific example?"
   - "어떤 파일이나 데이터를 사용하시나요?" / "What files or data do you work with?"
   - "결과물은 어떤 형태여야 하나요?" / "What should the output look like?"

4. **Define success criteria**:
   - "이 도구가 완성되면 무엇이 달라질까요?" / "What will be different when this tool is complete?"
   - "어떻게 하면 '잘 작동한다'고 판단할 수 있을까요?" / "How will you know it's working correctly?"

**Example conversation**:
```
AI: 무엇을 자동화하고 싶으신가요?

User: 매일 아침 페이스북이랑 인스타그램에서 좋아요, 댓글 수를 확인해서
      엑셀로 정리하는데 2시간 걸려요.

AI: 구체적으로 어떤 데이터를 수집하시나요?

User: 페이스북 페이지 "우리회사" 좋아요 수, 댓글 수, 공유 수랑
      인스타그램 계정 @ourcompany 좋아요, 댓글 수요.

AI: 엑셀 파일은 어떤 형태로 만드시나요?

User: 날짜별로 행을 만들고, 플랫폼별로 열을 나눠요.
      [Shows example screenshot]

AI: 완벽합니다. 이 도구가 완성되면 버튼 하나로 리포트가 생성되는 거죠?

User: 네! 5분 안에 끝나면 좋겠어요.
```

**Output of this step**: Clear understanding of:
- What to build
- Why (pain point / goal)
- Success criteria

---

### Step 3: Create Scenarios

**Goal**: Transform requirements into concrete, testable scenarios.

**Process**:

1. **Load planning guide** (for your reference):
   ```
   Read: references/planning-guide.md (Step 2: Scenarios section)
   ```

2. **Load domain examples** (for inspiration):
   ```
   Read: references/scenario-examples.md
   ```
   Find examples matching user's domain (marketing, finance, sales, etc.)

3. **Draft scenarios** collaboratively with user:
   - Start with **main scenario** (most common/important use case)
   - **Golden Path Prevention**: Ask if one-time or reusable
     - "Is this a one-time task or will you do this regularly?"
     - Build general tools, not one-off scripts
     - See planning-guide.md "Golden Path Prevention" section
   - Add **edge cases** or **variations** as additional scenarios
   - Aim for 2-4 scenarios for initial plan

4. **Scenario structure** (use planning-guide.md as reference):
   ```
   SCN-001: [Descriptive name]

   Description: [What happens - be specific]

   Input: [Concrete examples of files, data, config]

   Expected Output: [Specific file paths, content, format]

   Steps:
   1. [User action or system behavior]
   2. [User action or system behavior]
   3-5 more steps
   ```

5. **Validate scenarios with user**:
   - "이 시나리오가 실제 사용 방법과 맞나요?" / "Does this match how you'd actually use it?"
   - "빠진 경우가 있나요?" / "Are there any cases I'm missing?"

**Example scenario** (continuing the social media example):
```
SCN-001: Daily Facebook and Instagram engagement report

Description: User wants combined engagement metrics from Facebook and Instagram

Input:
- Facebook page: "우리회사" (last 24 hours)
- Instagram account: "@ourcompany" (last 24 hours)
- API credentials in .env file

Expected Output:
- Excel file: reports/engagement-2025-10-26.xlsx
- Contains: Likes, comments, shares, reach for each platform
- Summary row with total engagement score

Steps:
1. User runs: python src/report_generator.py
2. Tool authenticates with Facebook and Instagram APIs
3. Tool fetches metrics from last 24 hours
4. Tool calculates total engagement score
5. Tool generates Excel file with two sheets (Summary, Details)
6. Tool saves to reports/ directory
7. Tool shows success message: "리포트 생성 완료: reports/engagement-2025-10-26.xlsx"
```

---

### Step 4: Break Down into Tasks

**Goal**: Decompose scenarios into implementable tasks.

**Process**:

1. **AI makes technical decisions internally** (before breaking down tasks):
   ```
   Read: references/planning-guide.md (Step 1.5: AI Auto-Select Technical Approach)
   ```

   **Key**: User chooses business trade-offs, not technical details.
   - AI decides which libraries to use (pandas vs csv, requests vs urllib)
   - AI presents trade-offs in business language ("30-second install vs faster processing")
   - User confirms business value, not technical choice

2. **Analyze each scenario** to identify components:
   - Data input (file reading, API calls, config)
   - Data processing (transformation, calculation, validation)
   - Data output (file writing, visualization, reporting)
   - Error handling (validation, logging, user feedback)

3. **Create tasks** using this structure:
   ```
   Task N: [Descriptive name]

   Related Scenarios: SCN-001, SCN-002

   Description: [What needs to be implemented]

   Acceptance Criteria:
   - [ ] Specific, testable criterion 1
   - [ ] Specific, testable criterion 2

   Implementation Notes:
   [Libraries to use, approaches to consider]

   AI Note:
   Implement using TDD:
   - Write test for each validation criterion
   - Cover scenarios: SCN-XXX, SCN-YYY
   - Tag tests with @pytest.mark.scnXXX
   ```

4. **Review tasks with user**:
   - Explain each task in non-technical language
   - Confirm understanding and priority
   - Adjust scope if needed

**Example tasks** (for the social media scenario):
```
Task 1: Facebook API Integration

Related Scenarios: SCN-001

Description: Connect to Facebook to get page engagement data

Acceptance Criteria:
- [ ] Can log in to Facebook using credentials from .env file
- [ ] Can download likes, comments, shares for page "우리회사"
- [ ] Can filter by last 24 hours
- [ ] Returns data in a format we can use (list or table)

Implementation Notes:
- Use facebook-sdk library (will install with: pip install facebook-sdk)
- Get API credentials from Facebook Developer Portal
- Handle errors if Facebook is down or credentials are wrong

AI Note:
Implement using TDD:
- Write test for each acceptance criterion
- Cover scenarios: SCN-001
- Tag tests with @pytest.mark.scn001

---

Task 2: Instagram API Integration

Related Scenarios: SCN-001

Description: Connect to Instagram to get account engagement data

Acceptance Criteria:
- [ ] Can log in to Instagram using credentials from .env file
- [ ] Can download likes and comments for @ourcompany
- [ ] Can filter by last 24 hours
- [ ] Returns data in a format we can use

Implementation Notes:
- Use instagram-private-api library
- Handle Instagram rate limits (pause if needed)

AI Note:
Implement using TDD:
- Write test for each acceptance criterion
- Cover scenarios: SCN-001
- Tag tests with @pytest.mark.scn001

---

Task 3: Excel Report Generator

Related Scenarios: SCN-001

Description: Create Excel file with engagement data

Acceptance Criteria:
- [ ] Creates file in reports/ folder with today's date
- [ ] Has two sheets: "Summary" and "Details"
- [ ] Summary shows total engagement across platforms
- [ ] Details shows breakdown by platform
- [ ] File can be opened in Excel without errors

Implementation Notes:
- Use openpyxl library (pip install openpyxl)
- Format numbers with commas for readability
- Add headers in Korean

AI Note:
Implement using TDD:
- Write test for each acceptance criterion
- Cover scenarios: SCN-001
- Tag tests with @pytest.mark.scn001
```

---

### Step 5: Define Verification

**Goal**: Specify how to test each scenario.

**Process**:

1. **For each scenario**, define:
   - Command to run
   - Expected result (specific file paths, content, behavior)

2. **Verification structure**:
   ```
   SCN-001 Verification

   Command to run:
   ```bash
   python src/report_generator.py
   ```

   Expected result:
   - File created: reports/engagement-2025-10-26.xlsx
   - File opens without errors
   - Summary sheet shows total > 0
   - Details sheet has 2 rows (Facebook + Instagram)
   ```

**Why this matters**:
- Gives clear acceptance criteria for implementation
- Makes it easy to know when scenario is complete
- Provides test cases for debugging

---

### Step 6: Generate Plan Document

**Goal**: Create PLN-XXX document with all gathered information.

**Process**:

1. **Get next Plan ID**:
   ```bash
   python scripts/get_next_plan_id.py
   ```
   Output: `PLN-001` (or PLN-002, PLN-003, etc.)

2. **Ask user for plan name**:
   - Korean: "이 계획의 이름을 정해주세요 (예: daily-report-automation)"
   - English: "What should we name this plan? (e.g., daily-report-automation)"

3. **Load template**:
   ```
   Read: assets/plan-template.md
   ```

4. **Fill in template** with:
   - **YAML frontmatter**:
     - plan_id: PLN-XXX
     - status: pending
     - created: YYYY-MM-DD
     - updated: YYYY-MM-DD
     - language: python
     - author: (from CLAUDE.md or git config)
     - verified: false
     - verification_date: null
     - blocked_reason: null
   - **Plan content**:
     - Plan name
     - Requirements (from Step 2)
     - Scenarios (from Step 3)
     - Tasks (from Step 4)
     - Verification (from Step 5)

5. **Create plan file**:
   ```bash
   python scripts/create_plan.py <plan_id> <plan_name>
   ```

   Or write directly:
   ```
   Write: docs/plans/PLN-XXX-YYYY-MM-DD-name.md
   ```

6. **Confirm with user**:
   - Korean: "계획 문서를 생성했습니다: docs/plans/PLN-001-2025-10-26-daily-report.md"
   - English: "Created plan document: docs/plans/PLN-001-2025-10-26-daily-report.md"

---

### Step 7: Complexity Assessment

**Goal**: Evaluate plan complexity and offer simplification options.

**Process**:

1. **Calculate metrics**:
   - Total tasks: Count tasks in plan
   - Estimated time: ~10-15 min per task (rough estimate)
   - Scenarios: Count scenarios
   - Dependencies: Count external libraries needed

2. **Assess complexity**:
   - **Simple**: 1-3 tasks, 0-1 dependencies, < 30 min
   - **Medium**: 4-6 tasks, 2-3 dependencies, 30-90 min
   - **Complex**: 7+ tasks, 4+ dependencies, > 90 min

3. **Present to user** (in their language):
   ```
   Korean:
   이 계획의 복잡도:
   - 태스크: 5개
   - 예상 시간: 약 60분
   - 복잡도: 중간

   괜찮으신가요, 아니면 더 간단하게 만들까요?
   1. 이대로 진행 (전체 구현)
   2. 간단하게 만들기 (핵심 기능만)
   3. 단계별로 나누기 (PLN-001 간단 → PLN-002 추가 기능)
   ```

4. **If user chooses simplify**:
   - Remove edge case scenarios (keep happy path only)
   - Reduce tasks to minimum
   - Mark removed features for future plan (PLN-002)

5. **If user chooses split**:
   - Create PLN-001 with core features
   - Note additional features for PLN-002
   - Explain benefits: "먼저 핵심 기능을 만들고 테스트하는 게 안전합니다"

---

### Step 8: Git Commit

**Goal**: Commit the plan document for version control.

**Process**:

1. **Check git status**:
   ```bash
   git status
   ```

2. **Add and commit plan**:
   ```bash
   git add docs/plans/PLN-XXX-YYYY-MM-DD-name.md
   git commit -m "plan(PLN-XXX): add implementation plan for [feature name]"
   ```

3. **Inform user**:
   - Korean: "계획 문서를 커밋했습니다. 버전 관리가 시작되었습니다."
   - English: "Plan document committed. Version control started."

---

### Step 9: Next Steps Guidance

**Goal**: Guide user to implementation.

**Process**:

1. **Summarize what was created**:
   - Plan ID and file location
   - Number of scenarios and tasks
   - What the tool will do

2. **Explain next steps**:
   ```
   계획 작성 완료! ✅

   다음 단계:
   1. [implement] 스킬로 계획을 코드로 구현하기
   2. 구현 중 문제가 생기면 [debug] 스킬 사용하기
   3. 새로운 기능 추가는 새 계획(PLN-002)으로 작성하기

   "implement 스킬을 사용하고 싶습니다" 또는 "/implement"를 입력하세요.
   ```

3. **Remind about plan document**:
   - "계획 문서(docs/plans/PLN-001-...)는 언제든 수정할 수 있습니다"
   - "구현하면서 새로운 시나리오가 생각나면 추가하세요"

---

## Key Principles

### Documentation = Source of Truth

**Plans are living documents**:
- Store in `docs/plans/` with Plan ID for traceability
- Update as requirements evolve
- Reference in git commits: "Implement Task 1 from PLN-001"

### Scenario-Driven Planning

**Scenarios are the bridge** between vague requirements and concrete implementation:
- Vague: "자동화하고 싶어요" → Too abstract to implement
- Scenario: Specific input → steps → output → Implementable
- Task: Decomposed scenario → Codeable

### Progressive Disclosure

**Start simple, iterate**:
- Don't plan everything upfront
- Create minimal plan (2-3 scenarios) to start
- Add scenarios (PLN-002, PLN-003) as you learn from usage

**Example**:
```
PLN-001: Core functionality (2 scenarios, 4 tasks)
→ Implement and test
PLN-002: Add email delivery (1 scenario, 2 tasks)
→ Build on PLN-001
PLN-003: Add scheduling (1 scenario, 2 tasks)
→ Build on PLN-002
```

### User Language, Not Jargon

**Bad** (technical):
```
Task: Implement REST API client with OAuth2 flow
```

**Good** (user's language):
```
Task: Facebook 로그인 설정
Description: 페이스북에서 데이터를 가져올 수 있도록 연결 설정
```

---

## Troubleshooting

### User requirements are too vague

**Symptom**: "자동화하고 싶어요" without specifics

**Solution**:
1. Ask for concrete example: "지난주에 했던 작업을 예로 들어주세요"
2. Request sample files: "사용하는 파일을 보여주실 수 있나요?"
3. Show domain examples from `scenario-examples.md`

---

### User wants to build everything at once

**Symptom**: Long list of features, complex requirements

**Solution**:
1. Identify core use case: "가장 자주 사용할 기능은 무엇인가요?"
2. Suggest phased approach:
   - PLN-001: Core functionality only
   - PLN-002: Additional features later
3. Explain benefits: "먼저 핵심 기능을 만들고 테스트해보는 게 안전합니다"

---

### Scenarios are still too abstract

**Symptom**: Scenario lacks specific inputs/outputs

**Bad scenario**:
```
SCN-001: Generate report
User runs tool and gets report
```

**Solution**:
1. Ask for specifics:
   - "어떤 파일을 사용하나요?" → Input
   - "결과 파일 이름은?" → Output
   - "어떤 데이터가 들어있나요?" → Content
2. Show example from `scenario-examples.md`
3. Use 5W1H: Who, What, When, Where, Why, How

**Good scenario**:
```
SCN-001: Generate daily Facebook engagement report

Input:
- Facebook page: "MyBrand"
- Date: Today
- Credentials: .env file

Expected Output:
- File: reports/facebook-2025-10-26.xlsx
- Contents: Likes, comments, shares, reach
- Format: Excel with header row

Steps:
1. User runs: python src/facebook_report.py
2. Tool logs in to Facebook
3. Tool downloads today's metrics
4. Tool saves to Excel
5. Tool shows: "리포트 생성: reports/facebook-2025-10-26.xlsx"
```

---

### User asks about implementation details during planning

**Symptom**: "어떤 라이브러리를 써야 하나요?" "어떻게 코딩하나요?"

**Solution**:
1. Acknowledge: "좋은 질문입니다. 구현 단계에서 다룰게요"
2. Focus on "what", not "how": "지금은 '무엇을' 만들지 정하는 단계입니다"
3. Defer to implement skill: "구현 방법은 implement 스킬에서 안내해드립니다"
4. Add implementation notes to task if helpful

---

## Resources

### assets/
- `plan-template.md` - Plan document template with sections for requirements, scenarios, tasks, verification

### scripts/
- `get_next_plan_id.py` - Calculate next Plan ID by scanning docs/plans/
- `create_plan.py` - Generate plan file from template with Plan ID and name

### references/
- `planning-guide.md` - Detailed guide for transforming requirements → scenarios → tasks
- `scenario-examples.md` - Domain-specific scenario examples (marketing, finance, sales, HR, data processing)

---

## Example Session

```
User: /plan

AI: [Loads plan skill and user context from CLAUDE.md]

AI: 무엇을 자동화하고 싶으신가요? 현재 어떤 작업을 하고 계시고,
    어떤 부분이 불편하신가요?

User: 매일 아침 페이스북이랑 인스타그램 좋아요 수 확인해서 엑셀로 정리해요.
      2시간 걸려서 너무 오래 걸려요.

AI: 구체적으로 어떤 데이터를 수집하시나요?

User: 페이스북 페이지 "우리회사" 좋아요, 댓글, 공유 수랑
      인스타그램 @ourcompany 좋아요, 댓글이요.

AI: 엑셀 파일은 어떤 형태로 만드시나요?

User: 날짜별로 행 만들고, 플랫폼별로 열 나눠요.

AI: [Creates scenarios collaboratively]

    제가 이해한 걸 정리해볼게요:

    SCN-001: 페이스북 + 인스타그램 일일 리포트

    입력:
    - 페이스북 페이지: "우리회사"
    - 인스타그램: @ourcompany
    - 기간: 지난 24시간

    출력:
    - 파일: reports/engagement-2025-10-26.xlsx
    - 내용: 좋아요, 댓글, 공유 수 (플랫폼별)

    이렇게 하면 될까요?

User: 네 맞아요!

AI: [Breaks down into tasks, defines verification]

AI: [Generates PLN-001 document]

    계획 문서를 생성했습니다:
    docs/plans/PLN-001-2025-10-26-social-media-report.md

    3개 태스크로 나뉩니다:
    1. 페이스북 연동
    2. 인스타그램 연동
    3. 엑셀 리포트 생성

    다음 단계: implement 스킬로 코드 작성하기
    "/implement"를 입력하세요.
```
