# Debugging Guide

This guide provides a systematic approach to debugging errors in Python automation tools.

## The Debugging Process

```
Reproduce → Collect Info → Analyze → Hypothesize → Fix → Verify
```

---

## Step 1: Reproduce the Error

**Goal**: Consistently reproduce the error to understand it.

**Questions to ask user**:
- "어떤 명령어를 실행했을 때 오류가 발생했나요?" / "What command did you run when the error occurred?"
- "오류 메시지를 보여주실 수 있나요?" / "Can you show me the error message?"
- "매번 같은 오류가 나나요, 아니면 가끔 나나요?" / "Does this error happen every time or sometimes?"

**Try to reproduce**:
```bash
# Run the exact command user ran
python src/report_generator.py
```

**If can't reproduce**:
- Ask about environment differences
- Check Python version, installed packages
- Ask for screenshots or full error messages

---

## Step 2: Collect Information

**Goal**: Gather all relevant context about the error.

### Read the Error Message

**Anatomy of a Python error**:
```
Traceback (most recent call last):
  File "src/report_generator.py", line 23, in <module>
    data = client.fetch_data()
  File "src/facebook_client.py", line 45, in fetch_data
    response = requests.get(url)
AttributeError: 'NoneType' object has no attribute 'get'
```

**Key parts**:
1. **Traceback**: Shows the sequence of function calls
2. **File and line**: Where the error occurred (`facebook_client.py:45`)
3. **Error type**: `AttributeError`
4. **Error message**: `'NoneType' object has no attribute 'get'`

**Extract**:
- Error type (AttributeError, KeyError, FileNotFoundError, etc.)
- File and line number where error occurred
- What operation was being attempted

---

### Check Logs

**If logging is set up**:
```bash
cat logs/app.log | tail -50
```

Look for:
- Last successful operation before error
- Any warnings leading up to error
- Stack traces

---

### Check Environment

**Python version**:
```bash
python --version
```

**Installed packages**:
```bash
pip list
```

**Environment variables**:
```bash
# Check if .env file exists and has required keys
cat .env
```

---

## Step 3: Analyze Root Cause

**Goal**: Understand WHY the error happened, not just WHERE.

### Common Error Patterns

#### Pattern 1: NoneType Error
```
AttributeError: 'NoneType' object has no attribute 'get'
```

**Meaning**: A variable is `None` when code expected an object.

**Common causes**:
- Function returned `None` instead of expected value
- Forgot to return a value from a function
- Failed to handle case where data is missing

**How to find**:
- Look at the line before the error
- What function returned `None`?
- Why did it return `None`?

---

#### Pattern 2: KeyError
```
KeyError: 'likes'
```

**Meaning**: Trying to access a dictionary key that doesn't exist.

**Common causes**:
- API response structure changed
- Typo in key name
- Missing data in response

**How to fix**:
- Check what keys are actually in the dictionary
- Use `.get()` instead of `[]` to avoid error:
  ```python
  # Bad - crashes if 'likes' missing
  likes = data['likes']

  # Good - returns None if 'likes' missing
  likes = data.get('likes', 0)  # default to 0
  ```

---

#### Pattern 3: FileNotFoundError
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/input.csv'
```

**Meaning**: Trying to open a file that doesn't exist.

**Common causes**:
- File path is wrong
- File wasn't created yet
- Working directory is different than expected

**How to fix**:
- Check if file exists: `ls data/input.csv`
- Use absolute paths or `Path` from pathlib
- Create directory if needed: `mkdir -p data`

---

#### Pattern 4: Import Error
```
ModuleNotFoundError: No module named 'openpyxl'
```

**Meaning**: Python package is not installed.

**How to fix**:
```bash
pip install openpyxl
```

Add to requirements.txt:
```
openpyxl==3.1.2
```

---

#### Pattern 5: Type Error
```
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Meaning**: Trying to use incompatible types together.

**Common causes**:
- Adding string and number
- Passing wrong type to function

**How to fix**:
- Convert types explicitly:
  ```python
  # Bad
  total = 100 + "50"  # Error!

  # Good
  total = 100 + int("50")  # 150
  ```

---

### Use Print Debugging

**Add print statements to see what's happening**:

```python
def fetch_data(page_id):
    print(f"[DEBUG] Fetching data for page_id: {page_id}")

    url = build_url(page_id)
    print(f"[DEBUG] URL: {url}")

    response = requests.get(url)
    print(f"[DEBUG] Response status: {response.status_code}")
    print(f"[DEBUG] Response body: {response.text[:200]}")  # First 200 chars

    data = response.json()
    print(f"[DEBUG] Parsed data keys: {data.keys()}")

    return data
```

**Run again and check output**:
- Where does it fail?
- What are the actual values?
- Are they what you expected?

---

### Check Test Cases

**If tests exist**:
```bash
pytest tests/ -v
```

**Which tests are failing?**
- Same error as production?
- Different error?
- All passing but production fails?

This helps isolate the issue.

---

## Step 4: Form Hypothesis

**Goal**: Make an educated guess about what's wrong.

**Framework**:
1. **What**: What is the error? (AttributeError on None)
2. **Where**: Where does it happen? (facebook_client.py:45)
3. **Why**: Why does it happen? (requests.get() returned None instead of Response object)
4. **Hypothesis**: "The requests.get() is returning None, probably because URL is invalid or network error"

**Test hypothesis**:
- Add print statements to check URL
- Try the URL in browser
- Check network connectivity

---

## Step 5: Implement Fix

**Goal**: Fix the root cause, not just the symptom.

### Bad Fix (Symptom Only)
```python
# Just catching the error
try:
    response = requests.get(url)
    data = response.json()
except AttributeError:
    data = {}  # Return empty dict
```

**Problem**: Hides the real issue. User gets no data but no error either.

---

### Good Fix (Root Cause)
```python
# Handle the actual problem
response = requests.get(url, timeout=10)

if response.status_code != 200:
    raise ValueError(f"Failed to fetch data: HTTP {response.status_code}")

try:
    data = response.json()
except ValueError as e:
    raise ValueError(f"Invalid JSON response: {e}")

return data
```

**Why better**:
- Checks HTTP status
- Validates JSON
- Gives meaningful error messages
- User knows what went wrong

---

### Add Error Handling

**Defensive programming**:
```python
def fetch_engagement(page_id):
    # Validate input
    if not page_id:
        raise ValueError("page_id cannot be empty")

    # Check credentials
    if not self.api_key:
        raise ValueError("API key not configured. Check .env file")

    # Make request with timeout
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        raise ValueError("Request timed out. Check network connection")
    except requests.exceptions.ConnectionError:
        raise ValueError("Could not connect to API. Check internet connection")

    # Validate response
    if response.status_code == 401:
        raise ValueError("Invalid API credentials. Check .env file")
    elif response.status_code != 200:
        raise ValueError(f"API error: HTTP {response.status_code}")

    # Parse JSON safely
    try:
        data = response.json()
    except ValueError:
        raise ValueError("Invalid JSON response from API")

    return data
```

---

## Step 6: Verify Fix

**Goal**: Confirm the error is actually fixed.

### Run the Original Command
```bash
python src/report_generator.py
```

**Expected**: No error, produces output as intended.

---

### Run Tests
```bash
pytest tests/ -v
```

**Expected**: All tests pass.

---

### Test Edge Cases

**Try scenarios that might still fail**:
- Missing .env file
- Invalid API key
- Network disconnected
- Malformed data

**Each should give a clear error message**, not crash mysteriously.

---

## Step 7: Update Documentation

**Update architecture doc**:
```markdown
## Known Issues

### Facebook API Authentication
- **Error**: "Invalid API credentials"
- **Cause**: API key in .env is wrong or expired
- **Fix**: Get new API key from Facebook Developer Portal
```

**Update plan document** if behavior changed.

---

## Debugging Checklist

Before asking for help, check:

- [ ] Can you reproduce the error consistently?
- [ ] Do you have the full error message (not just last line)?
- [ ] Have you checked the file and line where error occurs?
- [ ] Have you added print statements to see variable values?
- [ ] Have you checked logs (if logging exists)?
- [ ] Have you verified environment (.env, Python version, packages)?
- [ ] Have you tested the fix?
- [ ] Have you run tests after fixing?

---

## When to Ask for Help

**Ask user for help when**:
- Need information only they have (API keys, file locations)
- Need to make a decision (which fix to use)
- Blocked by external issue (API down, permissions)

**Ask AI for help when**:
- Stuck after 2-3 attempts
- Error message is unclear
- Need library-specific knowledge

---

## Summary

**Good debugging workflow**:
1. **Reproduce** - Can you make it happen again?
2. **Collect** - Error message, logs, environment
3. **Analyze** - What's the root cause?
4. **Hypothesize** - Why is this happening?
5. **Fix** - Address root cause, not symptom
6. **Verify** - Test the fix thoroughly
7. **Document** - Record the issue and solution

**Key principle**: Understand before fixing. Don't guess blindly.
