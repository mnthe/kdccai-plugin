# Common Implementation Patterns

This guide provides ready-to-use code patterns for common automation tasks.

## File Operations

### Read CSV File

```python
import csv
from pathlib import Path

def read_csv(file_path):
    """Read CSV file and return list of dictionaries."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

# Usage
data = read_csv('data/input.csv')
print(data[0])  # First row as dict
```

---

### Write CSV File

```python
import csv

def write_csv(data, file_path, fieldnames):
    """Write list of dictionaries to CSV file."""
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Usage
data = [
    {'name': 'Alice', 'score': 95},
    {'name': 'Bob', 'score': 87}
]
write_csv(data, 'output.csv', fieldnames=['name', 'score'])
```

---

### Read Excel File (openpyxl)

```python
import openpyxl

def read_excel(file_path, sheet_name=None):
    """Read Excel file and return list of dictionaries."""
    wb = openpyxl.load_workbook(file_path)
    ws = wb[sheet_name] if sheet_name else wb.active

    # Get headers from first row
    headers = [cell.value for cell in ws[1]]

    # Read data rows
    data = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        row_dict = dict(zip(headers, row))
        data.append(row_dict)

    return data

# Usage
data = read_excel('data/sales.xlsx', sheet_name='Q1')
```

---

### Write Excel File (openpyxl)

```python
import openpyxl
from openpyxl.styles import Font, PatternFill

def write_excel(data, file_path, sheet_name="Sheet1"):
    """Write list of dictionaries to Excel file with formatting."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name

    if not data:
        wb.save(file_path)
        return

    # Write headers
    headers = list(data[0].keys())
    ws.append(headers)

    # Style headers
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font

    # Write data rows
    for row_data in data:
        ws.append([row_data[key] for key in headers])

    # Auto-adjust column widths
    for column_cells in ws.columns:
        length = max(len(str(cell.value or "")) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    wb.save(file_path)

# Usage
data = [
    {'Date': '2025-10-26', 'Platform': 'Facebook', 'Likes': 100},
    {'Date': '2025-10-26', 'Platform': 'Instagram', 'Likes': 150}
]
write_excel(data, 'reports/engagement.xlsx', sheet_name='Daily Report')
```

---

## Environment Variables (.env)

### Read from .env File

```python
from pathlib import Path
from dotenv import load_dotenv
import os

def load_config():
    """Load configuration from .env file."""
    # Find .env file in project root
    env_path = Path(__file__).parent.parent / '.env'

    if not env_path.exists():
        raise FileNotFoundError(f".env file not found at {env_path}")

    load_dotenv(env_path)

    # Get required variables
    config = {
        'facebook_api_key': os.getenv('FACEBOOK_API_KEY'),
        'instagram_api_key': os.getenv('INSTAGRAM_API_KEY'),
    }

    # Validate
    for key, value in config.items():
        if not value:
            raise ValueError(f"Missing {key} in .env file")

    return config

# Usage
config = load_config()
api_key = config['facebook_api_key']
```

**Example .env file**:
```
FACEBOOK_API_KEY=your_facebook_key_here
INSTAGRAM_API_KEY=your_instagram_key_here
```

---

## API Calls

### Basic GET Request

```python
import requests

def fetch_data(url, params=None, headers=None):
    """Make GET request and return JSON response."""
    response = requests.get(url, params=params, headers=headers, timeout=10)

    # Raise error if request failed
    response.raise_for_status()

    return response.json()

# Usage
data = fetch_data(
    'https://api.example.com/data',
    params={'date': '2025-10-26'},
    headers={'Authorization': f'Bearer {api_key}'}
)
```

---

### POST Request

```python
import requests

def post_data(url, data, headers=None):
    """Make POST request and return JSON response."""
    response = requests.post(url, json=data, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

# Usage
result = post_data(
    'https://api.example.com/submit',
    data={'name': 'Alice', 'score': 95},
    headers={'Authorization': f'Bearer {api_key}'}
)
```

---

### API with Retry Logic

```python
import requests
import time

def fetch_with_retry(url, max_retries=3, backoff=2):
    """Fetch data with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise  # Last attempt, re-raise error
            wait_time = backoff ** attempt
            print(f"Request failed, retrying in {wait_time}s... ({attempt + 1}/{max_retries})")
            time.sleep(wait_time)

# Usage
data = fetch_with_retry('https://api.example.com/data')
```

---

## Date and Time

### Get Today's Date

```python
from datetime import date, datetime

# Get today
today = date.today()
print(today)  # 2025-10-26

# Format as string
today_str = today.strftime('%Y-%m-%d')  # "2025-10-26"
today_kr = today.strftime('%Y년 %m월 %d일')  # "2025년 10월 26일"
```

---

### Date Range (Last N Days)

```python
from datetime import date, timedelta

def get_date_range(days=7):
    """Get list of dates for the last N days."""
    today = date.today()
    dates = []
    for i in range(days):
        d = today - timedelta(days=i)
        dates.append(d)
    return dates

# Usage
last_week = get_date_range(7)
print(last_week)  # [date(2025, 10, 26), date(2025, 10, 25), ...]
```

---

### Parse Date String

```python
from datetime import datetime

def parse_date(date_str, format='%Y-%m-%d'):
    """Parse date string to date object."""
    return datetime.strptime(date_str, format).date()

# Usage
d = parse_date('2025-10-26')
print(d)  # date(2025, 10, 26)

# Different format
d2 = parse_date('26/10/2025', format='%d/%m/%Y')
```

---

## Data Processing

### Filter List of Dictionaries

```python
# Filter by condition
data = [
    {'name': 'Alice', 'score': 95},
    {'name': 'Bob', 'score': 65},
    {'name': 'Charlie', 'score': 87}
]

# Get only high scores
high_scores = [row for row in data if row['score'] >= 80]
print(high_scores)  # [{'name': 'Alice', 'score': 95}, {'name': 'Charlie', 'score': 87}]
```

---

### Sum/Average

```python
scores = [95, 87, 65, 92, 78]

total = sum(scores)  # 417
average = sum(scores) / len(scores)  # 83.4
max_score = max(scores)  # 95
min_score = min(scores)  # 65
```

---

### Group By (using collections)

```python
from collections import defaultdict

data = [
    {'platform': 'Facebook', 'likes': 100},
    {'platform': 'Instagram', 'likes': 150},
    {'platform': 'Facebook', 'likes': 80},
]

# Group by platform
grouped = defaultdict(list)
for row in data:
    grouped[row['platform']].append(row['likes'])

print(dict(grouped))
# {'Facebook': [100, 80], 'Instagram': [150]}

# Calculate sum per platform
platform_totals = {platform: sum(likes) for platform, likes in grouped.items()}
print(platform_totals)
# {'Facebook': 180, 'Instagram': 150}
```

---

## Error Handling

### Try-Except Pattern

```python
def safe_divide(a, b):
    """Divide two numbers with error handling."""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None
    except TypeError:
        print("Error: Invalid input type")
        return None

# Usage
result = safe_divide(10, 2)  # 5.0
result = safe_divide(10, 0)  # Prints error, returns None
```

---

### File Exists Check

```python
from pathlib import Path

def read_file_safe(file_path):
    """Read file with existence check."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    return path.read_text(encoding='utf-8')

# Usage
try:
    content = read_file_safe('data/input.txt')
except FileNotFoundError as e:
    print(f"Error: {e}")
```

---

## Logging

### Basic Logging Setup

```python
import logging
from pathlib import Path

def setup_logging(log_file='logs/app.log'):
    """Set up logging to file and console."""
    # Create logs directory if needed
    Path(log_file).parent.mkdir(exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Also print to console
        ]
    )

# Usage
setup_logging()
logger = logging.getLogger(__name__)

logger.info("Starting report generation")
logger.warning("API rate limit approaching")
logger.error("Failed to fetch data")
```

---

## Progress Indication

### Simple Progress Messages

```python
def process_items(items):
    """Process items with progress messages."""
    total = len(items)

    for i, item in enumerate(items, 1):
        print(f"Processing {i}/{total}: {item}...")

        # Do work
        process(item)

    print(f"✅ Completed processing {total} items")

# Usage
process_items(['Facebook', 'Instagram', 'Twitter'])
# Output:
# Processing 1/3: Facebook...
# Processing 2/3: Instagram...
# Processing 3/3: Twitter...
# ✅ Completed processing 3 items
```

---

### tqdm Progress Bar

```python
from tqdm import tqdm
import time

def process_with_progress(items):
    """Process items with visual progress bar."""
    for item in tqdm(items, desc="Processing"):
        # Do work
        time.sleep(0.1)  # Simulate work

# Usage
process_with_progress(['item1', 'item2', 'item3'])
# Output:
# Processing: 100%|██████████| 3/3 [00:00<00:00, 10.2it/s]
```

---

## Command-Line Arguments

### argparse for CLI

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate engagement report')

    parser.add_argument('--date', type=str, default='today',
                        help='Date to generate report for (YYYY-MM-DD or "today")')
    parser.add_argument('--output', type=str, default='reports',
                        help='Output directory')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose logging')

    args = parser.parse_args()

    # Use arguments
    print(f"Generating report for: {args.date}")
    print(f"Output directory: {args.output}")

    if args.verbose:
        print("Verbose mode enabled")

if __name__ == '__main__':
    main()

# Usage:
# python src/report.py --date 2025-10-26 --output reports/ --verbose
```

---

## Summary of Common Libraries

| Task | Library | Install Command |
|------|---------|-----------------|
| CSV files | csv (built-in) | - |
| Excel files | openpyxl | `pip install openpyxl` |
| Environment variables | python-dotenv | `pip install python-dotenv` |
| HTTP requests | requests | `pip install requests` |
| Date/time | datetime (built-in) | - |
| Logging | logging (built-in) | - |
| Progress bars | tqdm | `pip install tqdm` |
| CLI arguments | argparse (built-in) | - |
