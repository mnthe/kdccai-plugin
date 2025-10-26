# Planning Guide

This guide explains how to transform user requirements into concrete implementation plans.

## The Planning Process

```
Requirements → Scenarios → Tasks → Verification
```

### Step 1: Requirements (What & Why)

**Goal**: Understand what the user wants to build and why.

**Questions to ask**:
- What problem are you solving?
- What does success look like?
- What are the constraints? (time, resources, technical)

**Output**: Clear problem statement and success criteria

**Example**:
```
What to Build: Daily marketing report automation
Why: Currently takes 2 hours every morning to collect data from 3 platforms
Success: One-click report generation in < 5 minutes
```

---

### Step 1.5: AI Auto-Select Technical Approach

**Goal**: AI makes technical decisions internally, presents trade-offs in business language.

**Key Principle**: **User chooses business trade-offs, not technical details**.

#### How It Works

1. **AI evaluates internally** (don't ask user about technical choices):
   - User's technical background (from CLAUDE.md)
   - Requirements complexity
   - Language (Python → pandas/openpyxl/requests)
   - File size, volume, performance needs

2. **AI selects approach**:
   - Simple automation → CSV module (built-in, no install)
   - Data processing → pandas (powerful, requires install)
   - API calls → requests (standard, requires install)

3. **AI presents in business language**:
   ```
   AI: I'll use a powerful data processing library for fast handling of large files.

   Trade-off:
   - Installation: 30 seconds on first run
   - After that: Instant execution
   - Can handle 1000+ files

   Is that okay?
   ```

4. **User confirms business trade-off**:
   - Installation time vs performance
   - Simplicity vs feature richness
   - File size limits

#### Examples

**❌ Bad (Technical Choice)**:
```
AI: Should we use pandas or csv module?
    - pandas: More features but requires installation
    - csv: Built-in but limited functionality

Which do you prefer?
```
**Problem**: User doesn't know what pandas is. Can't make informed choice.

---

**✅ Good (Business Trade-off)**:
```
AI: [Internally: Sees 100+ files → pandas needed]

AI: I'll use a data processing library that can handle large volumes.

Trade-off: 30-second installation first time, then very fast.

Your files are large, so this will save ~5 minutes per run.

Okay to install?

User: Yes (understands business value, not technical details)
```

#### When to Present Trade-offs

**DO present**:
- Installation time vs benefits
- Complexity vs features ("simple version vs full-featured")
- Performance trade-offs ("fast but uses more memory")
- Cost/limits ("free tier: 100 requests/day")

**DON'T ask about**:
- Which library to use (pandas vs csv vs polars)
- Which API method (REST vs GraphQL)
- Implementation patterns (OOP vs functional)
- Testing approach (unittest vs pytest)

**AI decides these internally** based on requirements and user's technical level.

---

### Step 2: Scenarios (How it will be used)

**Goal**: Create concrete examples of how the tool will be used.

**Key principle**: Scenarios should be **specific and testable**.

**Bad scenario** (too vague):
```
SCN-001: Generate report
- User runs the tool
- Report is created
```

**Good scenario** (specific and testable):
```
SCN-001: Generate daily Facebook and Instagram engagement report
Description: User wants combined engagement metrics from Facebook and Instagram

Input:
- Facebook page: "MyBrand" (last 24 hours)
- Instagram account: "@mybrand" (last 24 hours)
- API credentials in .env file

Expected Output:
- Excel file: reports/engagement-2025-10-26.xlsx
- Contains: Likes, comments, shares, reach for each platform
- Total engagement score calculated

Steps:
1. User runs: python src/report_generator.py
2. Tool authenticates with Facebook and Instagram APIs
3. Tool fetches metrics from last 24 hours
4. Tool generates Excel file with summary sheet
5. Tool saves to reports/ directory
```

**How many scenarios?**
- Simple project: 2-3 scenarios
- Complex project: 5-7 scenarios
- Start with the most important/common use case

#### Golden Path Prevention

**Problem**: Users often describe only their specific case, missing general use cases.

**Example**:
```
User: I want to merge these 3 specific Excel files: sales-jan.xlsx, sales-feb.xlsx, sales-mar.xlsx
```

**Risk**: Building a tool that only works for these 3 specific files.

**Solution**: Ask about generality.

```
AI: I see you want to merge these 3 files.

Question: Is this a one-time task, or will you do this regularly?

- One-time: I'll build a simple script for these 3 files
- Regular: I'll build a general tool that works with any files in a folder

User: Oh, I'll do this every quarter with different files.

AI: Perfect! I'll make it work with any Excel files in a folder.
   You can just drop files in and run it.

   Scenarios:
   - SCN-001: Merge 3 files (your current case)
   - SCN-002: Merge 10+ files (future quarters)
   - SCN-003: Handle empty files (edge case)
```

**When to ask**:
- User describes specific files/data
- User mentions specific dates/names
- User shows one example

**Questions to ask**:
- "Is this a one-time task or will you repeat it?"
- "Will the file names always be the same?"
- "Will you need this for other data later?"

**Goal**: Build tools that are reusable, not one-off scripts.

---

### Step 3: Tasks (What to implement)

**Goal**: Break scenarios into implementable chunks.

**Key principle**: Each task should contribute to one or more scenarios.

**Task structure**:
```
Task N: [Descriptive name]

Related Scenarios: SCN-001, SCN-002

Description: [What needs to be implemented]

Acceptance Criteria:
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2

Implementation Notes:
[Libraries, approaches, or technical details]
```

**Example**:
```
Task 1: Facebook API Integration

Related Scenarios: SCN-001

Description: Implement Facebook Graph API client to fetch page engagement metrics

Acceptance Criteria:
- [ ] Can authenticate with Facebook API using credentials from .env
- [ ] Can fetch likes, comments, shares, reach for a given page
- [ ] Can filter by date range (last 24 hours)
- [ ] Returns data in structured format (dict or dataclass)

Implementation Notes:
- Use facebook-sdk library (pip install facebook-sdk)
- Store API credentials in .env (never commit)
- Handle rate limiting with exponential backoff
- Log all API calls for debugging
```

**How to identify tasks**:
1. Read each scenario
2. Ask: "What components/functions are needed?"
3. Group related work into tasks
4. Ensure each task has clear acceptance criteria

**Common task categories**:
- Data fetching (API integration, file reading)
- Data processing (transformation, calculation, validation)
- Data output (file writing, visualization, reporting)
- Configuration (setup, credentials, parameters)
- Error handling (validation, logging, user feedback)

---

### Step 4: Verification (How to test)

**Goal**: Define how to verify each scenario works.

**Verification structure**:
```
SCN-001 Verification

Command to run:
```bash
python src/report_generator.py
```

Expected result:
- File created: reports/engagement-2025-10-26.xlsx
- Excel file contains 2 sheets: "Summary" and "Details"
- Summary sheet shows total engagement: 1,234
- Details sheet has 2 rows (Facebook + Instagram)
```

**Why verification matters**:
- Gives clear acceptance criteria for implementation
- Makes it easy to know when you're done
- Provides test cases for debugging

---

## Planning for Non-Developers

### Use User's Language

**Bad** (technical jargon):
```
Task: Implement REST API client with OAuth2 authentication
```

**Good** (user's language):
```
Task: Connect to Facebook to get page data
Description: Set up connection to Facebook so we can download likes and comments
```

### Provide Context

Non-developers may not know what's possible or what's needed.

**Provide examples**:
- "We'll need your Facebook API credentials. Here's how to get them: [link]"
- "The report will be an Excel file like this: [example screenshot]"

**Explain trade-offs**:
- "We can update data every hour, but Facebook limits how often we can check (rate limit)"
- "We can store data in Excel (easier to view) or CSV (easier to process later)"

### Start Simple, Iterate

**Phase 1**: Minimal viable version (1-2 scenarios)
**Phase 2**: Add features based on usage (more scenarios)

**Example**:
```
Phase 1 (PLN-001):
- SCN-001: Generate report for one platform (Facebook only)
- SCN-002: Save report as Excel file

Phase 2 (PLN-002):
- SCN-003: Add Instagram support
- SCN-004: Add email delivery

Phase 3 (PLN-003):
- SCN-005: Add scheduling (daily auto-run)
```

---

## Common Patterns

### Pattern 1: Data Processing Pipeline

```
Requirements: Transform data from format A to format B

Scenarios:
- SCN-001: Read input file
- SCN-002: Process/transform data
- SCN-003: Write output file
- SCN-004: Handle errors (missing file, invalid data)

Tasks:
- Task 1: File input reader
- Task 2: Data transformer
- Task 3: File output writer
- Task 4: Error handling and validation
```

### Pattern 2: API Integration

```
Requirements: Get data from external service

Scenarios:
- SCN-001: Authenticate with service
- SCN-002: Fetch data
- SCN-003: Handle rate limits
- SCN-004: Store/cache data

Tasks:
- Task 1: API client setup
- Task 2: Authentication flow
- Task 3: Data fetching with retry logic
- Task 4: Local caching mechanism
```

### Pattern 3: Scheduled Automation

```
Requirements: Run task on schedule

Scenarios:
- SCN-001: Manual run (for testing)
- SCN-002: Scheduled run (daily at 9am)
- SCN-003: Email notification on completion
- SCN-004: Error notification

Tasks:
- Task 1: Core automation logic
- Task 2: Scheduler setup (cron or Task Scheduler)
- Task 3: Email integration
- Task 4: Logging and error reporting
```

---

## Red Flags

**Too vague**:
- "Build a dashboard" → What data? What visualizations? For whom?
- "Automate the process" → What process? What are the steps?

**Too technical without context**:
- "Implement microservices architecture" → Why? Is this necessary for the goal?

**No success criteria**:
- How will you know it works?
- What's the minimum viable version?

**Skipping scenarios**:
- Going straight from requirements to code without concrete examples
- Results in mismatched expectations

---

## Checklist

Before finalizing a plan, verify:

- [ ] Requirements clearly state WHAT and WHY
- [ ] Success criteria are specific and measurable
- [ ] Scenarios are concrete and testable (specific inputs/outputs)
- [ ] Each scenario has 3-7 specific steps
- [ ] Tasks map to scenarios (traceability)
- [ ] Acceptance criteria are testable (not subjective)
- [ ] Verification commands are provided for each scenario
- [ ] Language is appropriate for the user's technical level
- [ ] Plan can be implemented incrementally (not all-or-nothing)
