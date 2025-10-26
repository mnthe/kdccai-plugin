---
name: project-init
description: Use when a non-developer user wants to create a new automation tool project. Sets up Python environment, project structure, and CLAUDE.md context file. Guides through environment setup → context gathering → structure initialization in user's preferred language.
---

# Project Init

## Overview

This skill initializes new automation tool projects for non-developers. It guides users through Python installation, gathers project context, and sets up a standardized documentation-driven project structure.

**Use this skill when:**
- User wants to start a new automation project
- User mentions creating a tool for their work
- User asks how to begin with AI-assisted coding

## Workflow

### Step 1: Check Python Installation

**Goal**: Ensure Python 3.12+ is installed before proceeding.

**Process**:

1. **Ask user about their operating system** (if not already known):
   - "어떤 운영체제를 사용하시나요? (Windows / macOS / Linux)"
   - "Which operating system are you using? (Windows / macOS / Linux)"

2. **Check if Python is installed**:
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **If Python is NOT installed or version < 3.12**:
   - Read the appropriate setup guide based on OS:
     - macOS: `assets/SETUP-python-macos.md`
     - Windows: `assets/SETUP-python-windows.md`
     - Linux: `assets/SETUP-python-linux.md`
   - **Present the setup instructions in user's preferred language**
   - Guide user through installation step by step
   - **Wait for user to complete installation and verify**

4. **If Python 3.12+ is installed**:
   - Confirm version: "Python 3.12.x가 설치되어 있습니다. 다음 단계로 진행하겠습니다."
   - Proceed to Step 2

**Important**:
- **Language constraint explanation**: Explain to user in their preferred language why we use Python:
  - Best for data processing and automation
  - Easy to install and use
  - Rich ecosystem for common tasks
  - TypeScript support can be added later if needed (e.g., n8n workflows)

---

### Step 2: Gather User Context

**Goal**: Understand user's background, work domain, and project goals to personalize guidance.

**Process**:

1. **Load the question reference**:
   ```
   Read: references/user-context-questions.md
   ```

2. **Ask questions naturally** (don't interrogate, have a conversation):
   - Preferred communication language
   - Work domain and tool purpose
   - Technical background
   - Confirm project type (Python-based local execution)

3. **Example conversation flow**:
   ```
   AI: 안녕하세요! 어떤 분야에서 일하시나요?
       그리고 이 도구로 무엇을 자동화하고 싶으신가요?

   User: 마케팅팀에서 일하고, 매일 리포트 만드는 걸 자동화하고 싶어요.

   AI: 좋습니다! 프로그래밍 경험이 있으신가요?

   User: 엑셀 함수는 쓸 줄 알지만 코딩은 처음이에요.

   AI: 알겠습니다. Python 기반으로 컴퓨터에서 직접 실행되는 도구를
       만들게 됩니다. 먼저 프로젝트 구조를 만들겠습니다...
   ```

4. **Store answers mentally** (you'll use them in Step 3)

**Reference**: `references/user-context-questions.md` contains detailed question flow and examples.

---

### Step 3: Create CLAUDE.md

**Goal**: Create a project-specific context file that will guide all future AI interactions.

**Process**:

1. **Load the template**:
   ```
   Read: assets/CLAUDE.md.template
   ```

2. **Fill in placeholders** with answers from Step 2:
   - `{{PREFERRED_LANGUAGE}}` → e.g., "한국어" or "English"
   - `{{WORK_DOMAIN}}` → e.g., "마케팅"
   - `{{TOOL_PURPOSE}}` → e.g., "매일 하는 리포트 자동화"
   - `{{TECHNICAL_BACKGROUND}}` → e.g., "엑셀 함수는 쓸 줄 알지만 코딩은 처음"
   - `{{PROJECT_TYPE}}` → "Python automation tool"
   - `{{DETAILED_TOOL_PURPOSE}}` → More detailed explanation if user provided
   - `{{KEY_REQUIREMENTS}}` → Specific requirements mentioned by user
   - `{{CONSTRAINTS}}` → Any constraints (time, resources, etc.)

3. **Write CLAUDE.md** to project root:
   ```
   Write: CLAUDE.md (with filled template)
   ```

4. **Confirm with user**:
   - "CLAUDE.md 파일을 생성했습니다. 이 파일은 앞으로 AI가 프로젝트를 이해하는 데 사용됩니다."
   - "Created CLAUDE.md file. This will help AI understand your project context."

---

### Step 4: Initialize Project Structure

**Goal**: Create standardized directory structure for documentation-driven development.

**Process**:

1. **Run the initialization script**:
   ```bash
   python scripts/init_structure.py
   ```

   Or if user wants a specific directory:
   ```bash
   python scripts/init_structure.py /path/to/project
   ```

2. **The script creates**:
   ```
   ├── docs/
   │   ├── knowledge-base/  # Domain knowledge, setup guides, API docs
   │   ├── plans/           # Implementation plans (PLN-XXX-YYYY-MM-DD-name.md)
   │   └── architecture/    # Component descriptions (how things work)
   ├── src/                 # Source code
   ├── tests/               # Test files
   └── .gitignore
   ```

3. **Create .gitignore**:
   ```
   Read: assets/gitignore-python.template
   Write: .gitignore (copy template content)
   ```

4. **Initialize git repository** (if not already initialized):
   ```bash
   git init
   git add .
   git commit -m "Initial project structure"
   ```

5. **Explain the structure to user** in their preferred language:
   - `docs/` - 모든 지식은 여기에 문서로 저장됩니다
   - `docs/plans/` - 구현 계획이 PLN-001, PLN-002 형식으로 저장됩니다
   - `src/` - 실제 코드가 들어갑니다
   - `tests/` - 테스트 파일이 들어갑니다

---

### Step 5: Next Steps Guidance

**Goal**: Guide user to the next skill (plan) and set expectations.

**Process**:

1. **Explain the overall workflow**:
   ```
   프로젝트 초기화 완료! ✅

   다음 단계:
   1. [plan] - 무엇을 만들지 구체적으로 계획하기
   2. [implement] - 계획을 코드로 구현하기
   3. [debug] - 문제가 생기면 해결하기

   "plan 스킬을 사용하고 싶습니다" 라고 말씀해주세요.
   ```

2. **Remind about CLAUDE.md**:
   - "CLAUDE.md 파일은 프로젝트 루트에 있습니다"
   - "앞으로 모든 AI 대화에서 이 파일을 참고합니다"
   - "필요하면 언제든 수정할 수 있습니다"

3. **Set expectations about Documentation = Source of Truth**:
   - 모든 지식은 문서(docs/)에 저장됩니다
   - 코드는 블랙박스 구현입니다
   - 변경사항은 문서에 먼저 또는 동시에 반영됩니다

---

## Key Principles

### Documentation-Driven Development

**All knowledge lives in docs, code is black box implementation.**

- `docs/knowledge-base/` - Domain knowledge, setup guides, API references
- `docs/plans/` - Implementation plans with Plan IDs (PLN-001, PLN-002, ...)
- `docs/architecture/` - How components work

**Why?**
- Non-developers understand documentation better than code
- AI can read docs to understand context without parsing code
- Changes are tracked in human-readable format

### Plan ID System

- Format: `PLN-001-YYYY-MM-DD-name.md`
- Auto-incremented (PLN-001, PLN-002, ...)
- Used in git commit messages for traceability
- Example: `PLN-001-2025-10-26-daily-report-automation.md`

### Language Constraint (Python)

**Month 1: Python only** (TypeScript deferred based on demand)

**Reasons explained to user**:
- Best for data processing and automation (primary use case)
- Easy to install and use
- Rich ecosystem for common automation tasks
- TypeScript support can be added as an extension if needed (e.g., n8n workflows)

### Communication Language

**All communication with user must be in their preferred language** (stored in CLAUDE.md).

- If user starts in Korean → Korean
- If user starts in English → English
- If unclear → Ask: "어떤 언어로 대화하는 것이 편하세요? (한국어 / English)"

---

## Troubleshooting

### Python installation fails

**macOS**:
- Homebrew permission issues → Don't use sudo, run `brew doctor`
- Command not found → Restart terminal, check PATH

**Windows**:
- "python not recognized" → Check "Add Python to PATH" was selected
- Permission denied → Run as Administrator or change execution policy

**Linux**:
- python3.12 not found → Add deadsnakes PPA (Ubuntu/Debian)
- venv module missing → Install python3.12-venv package

**Solution**: Refer user to the appropriate SETUP guide and walk through step-by-step.

### User has existing project structure

**Don't overwrite!**

1. Ask user if they want to:
   - Create in new directory
   - Merge with existing structure (careful!)
   - Skip structure creation (only create CLAUDE.md)

2. If merging:
   - Check for conflicts
   - Ask permission before creating each directory
   - Don't overwrite existing files

### User wants TypeScript instead of Python

**Explain the constraint**:
- Current version supports Python only
- TypeScript can be added later as an extension
- For n8n workflows, TypeScript can be integrated when needed

**If user insists**:
- Acknowledge the limitation
- Offer to proceed with Python and note TypeScript as future extension
- Or defer to program facilitator for special cases

---

## Resources Used

### assets/
- `CLAUDE.md.template` - Project context template
- `SETUP-python-macos.md` - macOS Python 3.12 installation guide
- `SETUP-python-windows.md` - Windows Python 3.12 installation guide
- `SETUP-python-linux.md` - Linux Python 3.12 installation guide
- `gitignore-python.template` - Python project .gitignore template

### scripts/
- `init_structure.py` - Cross-platform project structure initialization (Python)

### references/
- `user-context-questions.md` - Detailed user context gathering guide with examples

---

## Example Session

```
User: 새 프로젝트 시작하고 싶어요

AI: [Loads project-init skill]

AI: 좋습니다! 먼저 Python이 설치되어 있는지 확인하겠습니다.
    어떤 운영체제를 사용하시나요? (Windows / macOS / Linux)

User: macOS요

AI: [Checks Python version]
    Python 3.12.2가 설치되어 있습니다. ✅

    이제 프로젝트에 대해 몇 가지 여쭤볼게요.
    어떤 분야에서 일하시나요? 그리고 이 도구로 무엇을 자동화하고 싶으신가요?

User: 마케팅팀에서 일하고, 매일 여러 플랫폼에서 데이터 모아서
      리포트 만드는데 이걸 자동화하고 싶어요

AI: 좋은 프로젝트네요! 프로그래밍 경험이 있으신가요?

User: 엑셀 함수는 쓸 줄 아는데 코딩은 처음이에요

AI: 알겠습니다. Python 기반으로 진행됩니다.
    - 데이터 처리와 자동화에 최적화되어 있어요
    - 설치와 사용이 쉽습니다
    - 나중에 필요하면 TypeScript도 추가할 수 있습니다

    [Creates CLAUDE.md with context]
    [Runs init_structure.py]
    [Creates .gitignore]
    [Initializes git]

    프로젝트 초기화 완료! ✅

    다음 단계:
    1. [plan] - 무엇을 만들지 구체적으로 계획하기
    2. [implement] - 계획을 코드로 구현하기
    3. [debug] - 문제가 생기면 해결하기

    "plan 스킬을 사용하고 싶습니다" 라고 말씀해주세요.
```
