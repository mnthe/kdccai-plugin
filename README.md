# KDCCAI (KDC Club AI)

AI-assisted coding skills for non-developers. Build Python automation tools with guided workflows for project initialization, planning, implementation, and debugging.

## Overview

This Claude Code plugin provides a complete workflow for non-developers to create Python automation tools with AI assistance. It follows a "Documentation = Source of Truth" philosophy where all knowledge lives in docs, and code is the black box implementation.

## Features

### 🚀 Four Core Skills

1. **project-init** - Initialize new automation project
   - Python environment setup (3.12+)
   - Gather user context
   - Create CLAUDE.md context file
   - Set up project structure

2. **plan** - Create implementation plans
   - Gather requirements
   - Define concrete scenarios
   - Break down into tasks
   - Generate PLN-XXX documents

3. **implement** - Implement tasks with TDD
   - Task-by-task implementation
   - TDD internally (hidden from user)
   - Clean progress updates
   - Auto-update plan documents

4. **debug** - Systematic error debugging
   - Reproduce errors
   - Root cause analysis
   - Fix and verify
   - Document solutions

### 📁 Documentation-Driven Development

```
project/
├── CLAUDE.md                  # Project context for AI
├── docs/
│   ├── knowledge-base/        # Domain knowledge, API docs
│   ├── plans/                 # PLN-XXX implementation plans
│   └── architecture/          # How components work
├── src/                       # Source code (black box)
└── tests/                     # Test files (hidden from user)
```

### 🎯 Plan ID System

- Format: `PLN-001-YYYY-MM-DD-name.md`
- Auto-incremented tracking
- Referenced in git commits
- Maps to scenarios (SCN-001, SCN-002, ...)

## Installation

### Prerequisites

- [Claude Code CLI](https://docs.claude.com/en/docs/claude-code/installation)
- Python 3.12+ (will be installed during project-init if needed)

### Install Plugin

#### Option 1: From Marketplace (Recommended)

This plugin is hosted in the [KDCCAI Plugin Marketplace](https://github.com/mnthe/marketplace-for-kdccai).

1. **Add the marketplace** (one-time setup):
   ```bash
   /plugin marketplace add mnthe/marketplace-for-kdccai
   ```

2. **Install the plugin**:
   ```bash
   /plugin install kdccai@marketplace-for-kdccai
   ```

   Or browse and install interactively:
   ```bash
   /plugin
   ```

3. **Verify installation**:
   ```bash
   /plugin list
   ```

#### Option 2: Direct Installation from GitHub

```bash
/plugin install https://github.com/mnthe/kdccai-plugin
```

#### Option 3: Manual Installation

1. Clone this repository to your Claude plugins directory:
   ```bash
   git clone https://github.com/mnthe/kdccai-plugin ~/.claude/plugins/kdccai-plugin
   ```

2. The plugin will be automatically loaded by Claude Code on next restart.

## Quick Start

### 1. Initialize a New Project

```bash
cd ~/projects
mkdir my-automation-tool
cd my-automation-tool

# Initialize project
/project-init
```

The skill will guide you through:
- Python installation check
- User context gathering (language, domain, technical background)
- CLAUDE.md creation
- Project structure setup

### 2. Create Your First Plan

```bash
/plan
```

The skill will help you:
- Define what to automate
- Create concrete scenarios
- Break down into implementable tasks
- Generate `docs/plans/PLN-001-YYYY-MM-DD-name.md`

### 3. Implement the Plan

```bash
/implement
```

The skill will:
- Show you available plans
- Guide task-by-task implementation
- Use TDD internally (hidden from you)
- Show clean progress updates
- Auto-update plan document with completed tasks

### 4. Debug Issues

```bash
/debug
```

When errors occur, the skill will:
- Reproduce the error
- Analyze root cause
- Implement fix
- Verify fix works
- Document the solution

## Workflow Example

**Scenario**: Automate daily social media report

```bash
# 1. Initialize project
$ /project-init
AI: 어떤 분야에서 일하시나요?
User: 마케팅팀이요. 매일 페이스북, 인스타그램 리포트 만들어요.
AI: [Sets up project]

# 2. Create plan
$ /plan
AI: 무엇을 자동화하고 싶으신가요?
User: 페이스북, 인스타그램 좋아요 수 모아서 엑셀로 만들기
AI: [Creates PLN-001 with 3 tasks]

# 3. Implement
$ /implement
AI: PLN-001을 구현하겠습니다. Task 1부터 시작합니다...
AI: Task 1 완료 ✅ - Facebook API 연동
AI: Task 2 완료 ✅ - Instagram API 연동
AI: Task 3 완료 ✅ - Excel 리포트 생성
AI: 모든 태스크 완료!

# 4. Run your tool
$ python src/report_generator.py
✅ reports/engagement-2025-10-26.xlsx 생성 완료!
```

## Commands

| Command | Description |
|---------|-------------|
| `/project-init` | Initialize new automation project |
| `/plan` | Create implementation plan (PLN-XXX) |
| `/implement` | Implement tasks from plan using TDD |
| `/debug` | Debug errors systematically |

## Skills Reference

### project-init

**When to use**: Starting a new automation project

**What it does**:
1. Checks Python 3.12+ installation (guides install if needed)
2. Gathers user context (language, domain, technical level)
3. Creates CLAUDE.md with project context
4. Initializes docs/ structure
5. Sets up .gitignore and git repo

**Output**:
- CLAUDE.md
- docs/knowledge-base/, docs/plans/, docs/architecture/
- src/, tests/
- .gitignore

---

### plan

**When to use**: Before implementing new features or tools

**What it does**:
1. Loads user context from CLAUDE.md
2. Gathers requirements (what, why, success criteria)
3. Creates concrete scenarios with specific inputs/outputs
4. Breaks scenarios into implementable tasks
5. Defines verification commands
6. Generates PLN-XXX-YYYY-MM-DD-name.md

**Output**: Plan document in `docs/plans/`

**Key features**:
- Scenario-driven planning (SCN-001, SCN-002, ...)
- Task breakdown with acceptance criteria
- Verification steps
- Auto-incremented Plan IDs

---

### implement

**When to use**: After creating a plan, ready to code

**What it does**:
1. Loads plan document
2. Shows task list and gets user's choice
3. Implements each task using TDD (internally)
4. Shows clean progress updates (hides tests from user)
5. Marks tasks complete in plan document
6. Creates architecture documentation
7. Suggests git commit

**Output**:
- Working code in src/
- Tests in tests/ (hidden from user)
- Updated plan document (tasks marked done)
- Architecture doc in docs/architecture/

**Key features**:
- TDD internally, hidden from user
- Progressive implementation (one task at a time)
- Auto-marks tasks complete
- Domain-specific library recommendations

---

### debug

**When to use**: When errors occur

**What it does**:
1. Reproduces error
2. Collects info (error message, logs, environment)
3. Analyzes root cause (not just symptom)
4. Implements fix with validation
5. Verifies fix works
6. Documents issue and solution
7. Prevents similar errors

**Output**:
- Fixed code
- Updated tests
- Architecture doc with Known Issues

**Key features**:
- Systematic debugging methodology
- Common errors quick reference
- Root cause analysis
- Clear error messages

## Project Structure

```
kdccai-plugin/                   # Plugin root
├── .claude-plugin/
│   └── manifest.json            # Plugin metadata and configuration
├── .github/
│   └── workflows/
│       └── release.yml          # Automated release workflow
├── commands/
│   ├── project-init.md          # /project-init command
│   ├── plan.md                  # /plan command
│   ├── implement.md             # /implement command
│   └── debug.md                 # /debug command
├── skills/
│   ├── project-init/
│   │   ├── SKILL.md             # Skill instructions
│   │   ├── assets/              # Templates, .gitignore
│   │   ├── scripts/             # init_structure.py
│   │   └── references/          # User context questions, SETUP guides
│   ├── plan/
│   │   ├── SKILL.md
│   │   ├── assets/              # Plan template
│   │   ├── scripts/             # get_next_plan_id.py, create_plan.py
│   │   └── references/          # Planning guide, scenario examples
│   ├── implement/
│   │   ├── SKILL.md
│   │   ├── scripts/             # mark_task_done.py
│   │   └── references/          # TDD guide, common patterns, library recommendations
│   └── debug/
│       ├── SKILL.md
│       └── references/          # Debugging guide, common errors
├── LICENSE
└── README.md
```

## Design Philosophy

### Documentation = Source of Truth

**All knowledge lives in docs, code is black box**:
- `docs/knowledge-base/` - Domain knowledge, API docs
- `docs/plans/` - What to build (PLN-XXX)
- `docs/architecture/` - How it works
- `src/` - Implementation (don't read to understand)

**Why?**
- Non-developers understand docs better than code
- AI reads docs to understand context
- Changes tracked in human-readable format

### TDD (Hidden from User)

Tests are written first internally, but hidden from non-developers:
- AI writes tests → implements code → runs tests
- User only sees: "Task 1 완료 ✅"
- User doesn't see: pytest, test files, coverage

**Why?**
- Ensures code works before showing user
- Reduces cognitive load
- Focuses user on "what works" not "how we verify"

### Progressive Disclosure

Start simple, add complexity as needed:
- PLN-001: Core functionality (2-3 scenarios)
- PLN-002: Add features based on usage
- PLN-003: More features, automation, etc.

### User Language, Not Jargon

Adapt technical depth based on user's background:
- Non-technical: "설정 파일에 API 키 추가하세요"
- Semi-technical: "config.yaml에 facebook_api_key를 추가하세요"
- Technical: Full technical details

## Language Support

**Bilingual**: Korean and English
- Auto-detects user's preferred language from CLAUDE.md
- All skills support both languages
- Examples and error messages in user's language

## Target Audience

**Non-developers** who want to automate tasks:
- Marketing (social media reports, campaign tracking)
- Finance (expense reconciliation, budget reports)
- Sales (pipeline reports, commission calculation)
- HR (onboarding automation, inventory tracking)
- Data processing (file merging, format conversion)

**Technical background**: Minimal to none
- Can use Excel formulas
- Comfortable with copy-paste
- Willing to learn with guidance

## Requirements

### System Requirements

- **OS**: macOS, Windows, or Linux
- **Python**: 3.12+ (guided installation in project-init)
- **Claude Code**: Latest version

### Python Packages

Installed per-project based on needs:
- **File I/O**: openpyxl, pandas
- **APIs**: requests, domain-specific SDKs
- **Testing**: pytest (hidden from user)
- **Environment**: python-dotenv

## Development

### Plugin Manifest

The plugin configuration is defined in `.claude-plugin/manifest.json`:

```json
{
  "name": "kdccai-plugin",
  "version": "0.1.0",
  "description": "Claude plugin for KDC (Korea Digital Contents) club activity management and automation",
  "author": "Junghun Kim"
}
```

Required fields:
- `name`: Unique plugin identifier
- `version`: Semantic version number
- `description`: Brief description of the plugin
- `author`: Plugin creator or organization

### Versioning

This plugin uses semantic versioning (SemVer) and automated releases via GitHub Actions:

- Version format: `vMAJOR.MINOR.PATCH` (e.g., `v0.1.0`, `v1.0.0`)
- Releases are automatically created when version tags are pushed
- Each release includes the plugin files and installation instructions

### Creating a Release

This project supports two ways to create a release:

#### Option 1: Automated Release (Recommended)

Use GitHub Actions to automatically update files, create tag, and release:

1. Go to **Actions** tab in GitHub
2. Select **Release** workflow
3. Click **Run workflow**
4. Enter the version number (e.g., `0.2.0` - without 'v' prefix)
5. Click **Run workflow**

GitHub Actions will automatically:
- Update `manifest.json` to the specified version
- Generate/update `CHANGE_LOG.md` with commit history
- Commit the changes
- Create and push the version tag
- Create a GitHub release with installation instructions

#### Option 2: Manual Release

Follow these steps to manually prepare and tag a release:

1. **Update the version in `.claude-plugin/manifest.json`**
   ```bash
   # Edit the version field to match your new version (e.g., "0.2.0")
   nano .claude-plugin/manifest.json
   ```

2. **Update or create `CHANGE_LOG.md`** (optional but recommended)
   ```bash
   # Add a new entry at the top of CHANGE_LOG.md with your changes
   ```

3. **Commit the changes**
   ```bash
   git add .claude-plugin/manifest.json CHANGE_LOG.md
   git commit -m "chore: prepare release v0.2.0"
   ```

4. **Create and push the version tag**
   ```bash
   git tag v0.2.0
   git push origin main
   git push origin v0.2.0
   ```

5. **GitHub Actions will automatically:**
   - Verify that manifest.json version matches the tag
   - Create a GitHub release with installation instructions
   - Generate release notes from commits

**Important:** The version in `manifest.json` must match the tag version (without the 'v' prefix). For example, tag `v0.2.0` requires manifest version `0.2.0`. The release workflow will fail if versions don't match.

## Contributing

Contributions welcome! Please:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/my-feature`
3. **Follow existing skill structure**
4. **Test with real users** (non-developers)
5. **Submit pull request**

### Adding New Skills

1. Use skill-creator workflow
2. Follow progressive disclosure design
3. Include bilingual support (Korean + English)
4. Provide references, not just SKILL.md
5. Test with target audience

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Junghun Kim (mnthe)

## References

- [KDCCAI Plugin Marketplace](https://github.com/mnthe/marketplace-for-kdccai) - Official marketplace for installing this plugin
- [Claude Code Plugin Documentation](https://docs.claude.com/en/docs/claude-code/plugins-reference)
- [Claude Code Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)

---

**Made with ❤️ for non-developers who want to automate their work**
