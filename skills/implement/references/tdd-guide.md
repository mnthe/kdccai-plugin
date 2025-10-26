# TDD Guide (Hidden from User)

## Overview

Test-Driven Development (TDD) is used **internally** during implementation but **hidden from the user**. The user only sees progress updates, not test code.

**Why TDD?**
- Ensures code works before showing to user
- Catches errors early
- Provides confidence in implementation
- Makes debugging easier

**Why hide it?**
- Non-developers don't need to see test code
- Reduces cognitive load
- Focuses user on "what works" not "how we verify"

---

## TDD Workflow (Internal)

```
For each task:
1. Write test (hidden from user)
2. Run test → RED (fails)
3. Write minimal code to pass
4. Run test → GREEN (passes)
5. Refactor if needed
6. Show user: "Task X completed ✅"
```

---

## When to Write Tests

**Always write tests for**:
- Data transformation logic
- API integrations
- File I/O operations
- Calculations or business logic

**Can skip tests for**:
- Simple glue code (imports, basic assignments)
- Configuration files
- One-time setup scripts

---

## Test Organization

```
project/
├── src/
│   └── report_generator.py
└── tests/
    └── test_report_generator.py
```

**Test file naming**: `test_<module_name>.py`

**Test function naming**: `test_<what_it_tests>()`

---

## Example TDD Cycle

### Task: Fetch Facebook engagement data

**Step 1: Write test (hidden from user)**

```python
# tests/test_facebook_client.py
import pytest
from src.facebook_client import FacebookClient

def test_fetch_engagement_returns_dict():
    """Test that fetch_engagement returns a dictionary with expected keys."""
    client = FacebookClient(api_key="test_key")

    # Mock the API response
    with patch('src.facebook_client.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'likes': 100,
            'comments': 20,
            'shares': 5
        }

        result = client.fetch_engagement(page_id="test_page")

        assert isinstance(result, dict)
        assert 'likes' in result
        assert 'comments' in result
        assert 'shares' in result
        assert result['likes'] == 100
```

**Step 2: Run test → RED**

```bash
pytest tests/test_facebook_client.py
# FAILED - FacebookClient not implemented yet
```

**Step 3: Write minimal code**

```python
# src/facebook_client.py
import requests

class FacebookClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_engagement(self, page_id):
        # Minimal implementation to pass test
        response = requests.get(
            f"https://graph.facebook.com/{page_id}",
            params={'access_token': self.api_key}
        )
        return response.json()
```

**Step 4: Run test → GREEN**

```bash
pytest tests/test_facebook_client.py
# PASSED
```

**Step 5: Show user**

```
AI: Task 1 완료: 페이스북 API 연동 ✅
    페이스북 페이지에서 좋아요, 댓글, 공유 수를 가져올 수 있습니다.
```

**User never sees the test code** - only the result.

---

## Testing Patterns

### Pattern 1: Mocking External APIs

```python
from unittest.mock import patch, Mock

def test_api_call():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': 'test'}

        result = my_function()

        assert result == {'data': 'test'}
```

**Why**: Don't make real API calls in tests (slow, requires credentials)

---

### Pattern 2: File I/O Testing

```python
import tempfile
from pathlib import Path

def test_file_writing():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test.xlsx"

        generate_report(output_file)

        assert output_file.exists()
        # Optionally: load and verify contents
```

**Why**: Use temporary files to avoid polluting project directory

---

### Pattern 3: Pytest Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    """Fixture providing sample data for multiple tests."""
    return {
        'facebook': {'likes': 100, 'comments': 20},
        'instagram': {'likes': 150, 'comments': 30}
    }

def test_total_engagement(sample_data):
    total = calculate_total_engagement(sample_data)
    assert total == 300  # 100 + 20 + 150 + 30
```

**Why**: Reuse test data across multiple tests

---

### Pattern 4: Testing Error Cases

```python
def test_invalid_api_key_raises_error():
    client = FacebookClient(api_key="invalid")

    with pytest.raises(AuthenticationError):
        client.fetch_engagement(page_id="test")
```

**Why**: Verify error handling works correctly

---

## pytest Markers (for Scenario Tracking)

```python
@pytest.mark.scn001
def test_facebook_engagement():
    """Test for SCN-001: Daily Facebook report."""
    pass

@pytest.mark.scn002
def test_instagram_engagement():
    """Test for SCN-002: Instagram story metrics."""
    pass
```

**Run tests for specific scenario**:
```bash
pytest -m scn001
```

**Why**: Map tests to scenarios for traceability

---

## Communication with User

### ❌ Don't say:

```
AI: 테스트를 작성했습니다. test_facebook_client.py를 만들고...
    pytest를 실행해서 통과했습니다...
```

### ✅ Do say:

```
AI: Task 1 진행 중...
    [Internally: writes test, implements code, verifies]

    Task 1 완료 ✅
    페이스북 API 연동이 완료되었습니다.
```

**User experience**: Clean progress updates, not implementation details.

---

## When Tests Fail

**If test fails during development**:

1. **Debug internally** (don't show user raw error)
2. **Fix the code**
3. **Re-run test**
4. **Only then** show user "Task completed"

**If you can't fix after 2-3 attempts**:

```
AI: Task 1을 구현하는 중 문제가 발생했습니다.
    페이스북 API 인증 부분에서 오류가 나는데, API 키를 확인해주시겠어요?
```

Be specific about what's needed, but don't dump stack traces on the user.

---

## Running Tests

**During development (internal)**:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_facebook_client.py

# Run specific test
pytest tests/test_facebook_client.py::test_fetch_engagement

# Run tests for a scenario
pytest -m scn001

# Verbose output
pytest -v
```

**After implementation (show user)**:
```bash
# Verification command (in plan document)
python src/report_generator.py
```

The user runs the **actual script**, not pytest.

---

## Test Coverage (Internal Metric)

**Aim for**:
- Core logic: 80%+ coverage
- Edge cases: Test major error paths
- Integration: At least one end-to-end test per scenario

**Don't mention coverage % to user** - just ensure code works.

---

## Example: Full TDD Cycle for a Task

**Task**: Create Excel report with engagement data

**Internal TDD Process** (hidden from user):

```python
# 1. Write test
def test_generate_excel_report(sample_data, tmp_path):
    output = tmp_path / "report.xlsx"

    generate_excel_report(sample_data, output)

    assert output.exists()

    # Load and verify
    wb = openpyxl.load_workbook(output)
    assert "Summary" in wb.sheetnames
    assert "Details" in wb.sheetnames

# 2. Run → RED (function doesn't exist)

# 3. Implement
def generate_excel_report(data, output_path):
    wb = openpyxl.Workbook()

    # Summary sheet
    summary = wb.active
    summary.title = "Summary"
    summary['A1'] = "Total Engagement"
    summary['B1'] = sum(...)

    # Details sheet
    details = wb.create_sheet("Details")
    # ... populate details

    wb.save(output_path)

# 4. Run → GREEN (test passes)

# 5. Show user
```

**User sees**:
```
AI: Task 3 완료 ✅
    엑셀 리포트 생성 기능이 완성되었습니다.
    reports/ 폴더에 파일이 생성됩니다.
```

---

## Summary

**TDD is mandatory but invisible**:
- ✅ Always write tests
- ✅ Run tests to verify
- ✅ Only show user when GREEN
- ❌ Don't show test code to user
- ❌ Don't mention pytest in user-facing messages
- ✅ Show clean progress: "Task X 완료 ✅"

**The user's experience**: Smooth progress updates, working code, confidence it works.
