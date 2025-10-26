---
name: debug
description: Use when user encounters errors or bugs in their automation tool. Guides through systematic debugging: reproduce error → collect info → analyze root cause → fix → verify. Triggered by "/debug" command or error reports.
---

# Debug

## Overview

This skill helps non-developers systematically debug errors using a structured approach: reproduce, analyze, fix, and verify.

**Use this skill when:**
- User reports an error or bug
- User says "/debug" or "오류가 생겼어요"
- Code is not working as expected
- Tests are failing

**Output**: Fixed code, updated tests, clear explanation of what was wrong

---

## Workflow

### Step 1: Load Context

**Goal**: Understand the project and user's technical level.

**Process**:

1. **Read CLAUDE.md**:
   ```
   Read: CLAUDE.md
   ```

2. **Extract**:
   - Preferred communication language
   - Technical background (adjust explanation depth)
   - Work domain

3. **Ask about the error**:
   - Korean: "어떤 오류가 발생했나요? 오류 메시지를 보여주실 수 있나요?"
   - English: "What error occurred? Can you show me the error message?"

---

### Step 2: Reproduce the Error

**Goal**: Make the error happen consistently to understand it.

**Process**:

1. **Get the exact command that failed**:
   ```
   User: python src/report_generator.py 실행했는데 오류가 났어요
   ```

2. **Run the command**:
   ```bash
   python src/report_generator.py
   ```

3. **Capture full error message**:
   - Full traceback (all lines, not just last one)
   - Error type (AttributeError, KeyError, etc.)
   - File and line number
   - What operation was being attempted

4. **If error reproduces**:
   ```
   AI: 같은 오류를 재현했습니다. 원인을 분석하겠습니다.
   ```

5. **If error doesn't reproduce**:
   - Ask about environment differences
   - Check Python version, packages
   - Ask for screenshot of error

---

### Step 3: Collect Information

**Goal**: Gather all context needed to diagnose the problem.

**Process**:

1. **Read the debugging guide**:
   ```
   Read: references/debugging-guide.md (Step 2: Collect Information)
   ```

2. **Examine error location**:
   ```
   Read: src/facebook_client.py (around line 45 where error occurred)
   ```

3. **Check for related code**:
   - Read calling function
   - Read related modules
   - Check test files

4. **Check environment**:
   ```bash
   # Python version
   python --version

   # Installed packages
   pip list

   # Check .env file (without showing secrets)
   ls .env
   ```

5. **Check logs** (if exist):
   ```bash
   cat logs/app.log | tail -50
   ```

---

### Step 4: Analyze Root Cause

**Goal**: Understand WHY the error happened, not just WHERE.

**Process**:

1. **Load common errors reference**:
   ```
   Read: references/common-errors.md
   ```

   Find if this is a known error pattern.

2. **Examine the error type**:
   - **AttributeError on None** → Something returned `None` unexpectedly
   - **KeyError** → Dictionary key missing
   - **FileNotFoundError** → File path wrong or file doesn't exist
   - **ModuleNotFoundError** → Package not installed
   - **TypeError** → Wrong type used
   - **ValueError** → Invalid value

3. **Trace backwards**:
   ```python
   # Error at line 45:
   response = requests.get(url)  # Error: url is None

   # Where did url come from? Line 40:
   url = build_url(page_id)  # Returns None if page_id is invalid

   # Where did page_id come from? Line 30:
   page_id = config.get('facebook_page')  # Missing from config!

   # Root cause: 'facebook_page' not set in config
   ```

4. **Form hypothesis**:
   ```
   AI: 오류의 근본 원인을 찾았습니다:
       config.yaml에 'facebook_page' 설정이 없어서
       build_url()이 None을 반환했고,
       requests.get(None)이 실행되면서 오류가 발생했습니다.
   ```

5. **Verify hypothesis** with user:
   ```
   AI: config.yaml 파일을 확인해주실 수 있나요?
       'facebook_page' 항목이 있는지 확인해주세요.
   ```

---

### Step 5: Implement Fix

**Goal**: Fix the root cause, not just the symptom.

**Process**:

1. **Choose fix approach** based on root cause:

**Approach 1: Fix user's configuration**
```
AI: config.yaml에 이 설정을 추가해주세요:
    ```yaml
    facebook_page: "우리회사"
    ```
```

**Approach 2: Add validation and better error message**
```python
def build_url(page_id):
    if not page_id:
        raise ValueError(
            "Facebook page ID not configured. "
            "Add 'facebook_page' to config.yaml"
        )
    return f"https://graph.facebook.com/{page_id}"
```

**Approach 3: Add defensive check**
```python
# Before fix
url = build_url(page_id)
response = requests.get(url)

# After fix
url = build_url(page_id)
if not url:
    raise ValueError("Failed to build API URL. Check configuration.")

try:
    response = requests.get(url, timeout=10)
except requests.exceptions.Timeout:
    raise ValueError("API request timed out. Check network connection.")
```

2. **Explain fix to user**:
   - **Non-technical**: "설정 파일에 페이스북 페이지 이름을 추가하면 됩니다"
   - **Semi-technical**: "config.yaml에 facebook_page 설정을 추가하고, 코드에서도 validation을 추가했습니다"

3. **Update code**:
   ```
   Edit: src/facebook_client.py
   ```

4. **Update tests** (if TDD):
   ```python
   # Add test for error case
   def test_build_url_with_empty_page_id():
       with pytest.raises(ValueError, match="Facebook page ID not configured"):
           build_url("")
   ```

---

### Step 6: Verify Fix

**Goal**: Confirm the error is actually fixed.

**Process**:

1. **Run the original failing command**:
   ```bash
   python src/report_generator.py
   ```

   **Expected**: No error, produces output as intended.

2. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

   **Expected**: All tests pass.

3. **Test edge cases**:
   - What if config file doesn't exist?
   - What if value is wrong type?
   - What if network is down?

   Each should give **clear error message**, not crash mysteriously.

4. **Show user the fix worked**:
   ```
   AI: 수정 완료! ✅
       python src/report_generator.py 실행하면 정상 작동합니다.

       [Shows successful output]

       수정한 내용:
       1. config.yaml에 facebook_page 설정 추가
       2. 코드에서 설정 누락 시 명확한 오류 메시지 표시
   ```

---

### Step 7: Document the Issue

**Goal**: Record the problem and solution for future reference.

**Process**:

1. **Update architecture document**:
   ```
   Read: docs/architecture/PLN-XXX-implementation.md
   ```

   Add Known Issues section:
   ```markdown
   ## Known Issues

   ### Configuration Error: Missing facebook_page

   **Error**: `ValueError: Facebook page ID not configured`

   **Cause**: `facebook_page` not set in config.yaml

   **Solution**: Add to config.yaml:
   ```yaml
   facebook_page: "your_page_name"
   ```
   ```

2. **Update plan document** if needed:
   - If fix changes behavior
   - If new requirements discovered

3. **Add comment in code** if tricky:
   ```python
   # Note: page_id can be None if config is missing.
   # Validate early to give clear error message.
   if not page_id:
       raise ValueError("Facebook page ID not configured...")
   ```

---

### Step 8: Prevent Similar Errors

**Goal**: Make the code more robust to prevent similar issues.

**Process**:

1. **Add validation early**:
   ```python
   # Validate configuration at startup
   def validate_config(config):
       required = ['facebook_page', 'api_key']
       missing = [key for key in required if not config.get(key)]
       if missing:
           raise ValueError(f"Missing required config: {', '.join(missing)}")
   ```

2. **Improve error messages**:
   ```python
   # Bad
   raise ValueError("Invalid page")

   # Good
   raise ValueError(
       f"Invalid page ID: '{page_id}'. "
       f"Expected format: alphanumeric string. "
       f"Check 'facebook_page' in config.yaml"
   )
   ```

3. **Add logging**:
   ```python
   import logging
   logger = logging.getLogger(__name__)

   logger.info(f"Fetching data for page: {page_id}")
   logger.warning(f"Retry attempt {attempt}/3")
   logger.error(f"Failed to fetch data: {e}")
   ```

4. **Update tests**:
   ```python
   # Add tests for error cases
   def test_missing_config():
       ...

   def test_invalid_api_key():
       ...

   def test_network_error():
       ...
   ```

---

## Key Principles

### Understand Before Fixing

**DON'T**: Jump to conclusions or guess
```
AI: 아마도 API 키가 문제인 것 같아요 (guessing)
```

**DO**: Investigate systematically
```
AI: 오류 메시지를 보니 URL이 None입니다.
    build_url() 함수를 확인해보겠습니다.
    [Reads code]
    page_id가 None이네요. config 파일을 확인해주시겠어요?
```

---

### Fix Root Cause, Not Symptom

**Bad fix** (hides the problem):
```python
try:
    response = requests.get(url)
except Exception:
    return {}  # Silently return empty dict
```

**Good fix** (addresses root cause):
```python
if not url:
    raise ValueError("URL is None. Check config.yaml")

response = requests.get(url, timeout=10)
if response.status_code != 200:
    raise ValueError(f"API error: HTTP {response.status_code}")
```

---

### Clear Communication

**Adapt to user's technical level** (from CLAUDE.md):

**Non-technical**:
```
AI: 설정 파일에 페이스북 페이지 이름이 빠져있어요.
    config.yaml 파일을 열어서 이 줄을 추가해주세요:
    facebook_page: "우리회사"
```

**Semi-technical**:
```
AI: config.yaml에 'facebook_page' 키가 없어서
    build_url() 함수가 None을 반환했습니다.
    validation을 추가해서 명확한 오류 메시지가 나오도록 수정했습니다.
```

---

### Test the Fix

**Always verify**:
1. Run the original failing command → Should work
2. Run tests → Should all pass
3. Try edge cases → Should give clear errors

**Don't just assume it's fixed**. Actually test it.

---

## Troubleshooting

### Can't Reproduce Error

**Symptom**: User has error but you can't reproduce it.

**Solution**:
1. Ask for exact error message (screenshot)
2. Ask for exact command they ran
3. Check environment differences:
   - Python version
   - Installed packages (`pip list`)
   - OS (macOS vs Windows vs Linux)
   - Working directory
4. Ask user to run with verbose logging:
   ```bash
   python src/report_generator.py --verbose
   ```

---

### Fix Breaks Something Else

**Symptom**: Fixed one error but created another.

**Solution**:
1. Run full test suite: `pytest tests/ -v`
2. Check what broke
3. Either:
   - Fix the new issue
   - Or revert and find different solution

---

### Error is in External Library

**Symptom**: Error occurs inside a library (requests, openpyxl, etc.).

**Solution**:
1. Check library version: `pip show requests`
2. Check library documentation for changes
3. Try updating library: `pip install --upgrade requests`
4. Search GitHub issues for the library
5. Add workaround in your code if needed

---

### User Doesn't Understand Fix

**Symptom**: User says "I don't understand what to do".

**Solution**:
1. Break down into smaller steps
2. Show exact commands to run
3. Provide screenshots or examples
4. Offer to do it together step-by-step

**Example**:
```
AI: 3가지 단계로 수정하겠습니다:

    1단계: config.yaml 파일 열기
    → 파일 탐색기에서 프로젝트 폴더 열기
    → config.yaml 더블클릭

    2단계: 이 줄 추가하기
    → 파일 맨 아래에 다음 줄 추가:
      facebook_page: "우리회사"
    → 저장 (Ctrl+S)

    3단계: 다시 실행해보기
    → 터미널에서: python src/report_generator.py

    이해되셨나요? 각 단계별로 진행하면서 막히는 부분 있으면 말씀해주세요.
```

---

## Resources

### references/
- `debugging-guide.md` - Systematic debugging methodology (reproduce → collect → analyze → fix → verify)
- `common-errors.md` - Quick reference for frequent Python errors (FileNotFoundError, TypeError, KeyError, etc.) with solutions

---

## Example Session

```
User: /debug

AI: [Loads CLAUDE.md]

AI: 어떤 오류가 발생했나요? 오류 메시지를 보여주실 수 있나요?

User: python src/report_generator.py 실행하니까 이런 오류가 났어요:
      AttributeError: 'NoneType' object has no attribute 'get'

AI: [Reproduces error]

    같은 오류를 재현했습니다.

    [Reads error traceback]

    오류가 facebook_client.py 45번 줄에서 발생했네요.
    해당 코드를 확인하겠습니다.

    [Reads code]

    원인을 찾았습니다:
    - config.yaml에 'facebook_page' 설정이 없음
    - build_url()이 None을 반환
    - requests.get(None)에서 오류 발생

    config.yaml 파일에 페이스북 페이지 이름이 설정되어 있나요?

User: 아 없는 것 같아요

AI: 그럼 config.yaml에 이 설정을 추가해주세요:

    ```yaml
    facebook_page: "우리회사"
    ```

    그리고 코드도 수정해서, 다음에 이런 설정이 빠지면
    명확한 오류 메시지가 나오도록 하겠습니다.

    [Updates code with validation]

    수정 완료! ✅

    이제 python src/report_generator.py를 실행해보세요.
    정상 작동할 거예요.

User: 오 됐어요!

AI: 좋습니다! 수정한 내용:
    1. config.yaml에 facebook_page 추가
    2. 코드에서 설정 누락 시 명확한 오류 메시지 표시
    3. 테스트 추가해서 다음에는 이런 문제 조기 발견

    docs/architecture/에 이슈를 기록해뒀습니다.
```
