# Library Recommendations by Domain

This guide recommends Python libraries for common automation tasks based on domain and use case.

## File Processing

### Excel Files

**openpyxl** (Recommended for .xlsx files)
```bash
pip install openpyxl
```

**Use when**: Reading/writing Excel 2007+ (.xlsx) files

**Pros**:
- Full support for Excel features (formulas, charts, styles)
- Active development
- Good documentation

**Example use cases**:
- Generate formatted reports
- Read data from Excel templates
- Create charts and styled sheets

---

**pandas** (For data analysis)
```bash
pip install pandas openpyxl
```

**Use when**: Heavy data processing, analysis, transformation

**Pros**:
- Powerful data manipulation
- Easy filtering, grouping, aggregation
- Can read/write Excel, CSV, SQL

**Example use cases**:
- Merge multiple Excel files
- Pivot tables and aggregations
- Data cleaning and transformation

---

### CSV Files

**csv** (Built-in, no install needed)

**Use when**: Simple CSV reading/writing

**Pros**:
- No dependencies
- Fast
- Sufficient for most use cases

---

**pandas** (For complex processing)

**Use when**: Need data analysis features

---

### PDF Files

**PyPDF2** (Basic PDF operations)
```bash
pip install PyPDF2
```

**Use when**: Merge, split, rotate PDFs

**Not good for**: Extracting text (use pdfplumber instead)

---

**pdfplumber** (Extract text and data)
```bash
pip install pdfplumber
```

**Use when**: Extracting text, tables, or form data from PDFs

**Pros**:
- Excellent table extraction
- Character-level precision
- Good documentation

---

## Web APIs

### HTTP Requests

**requests** (Industry standard)
```bash
pip install requests
```

**Use when**: Making HTTP calls to APIs

**Pros**:
- Simple, intuitive API
- Built-in JSON handling
- Session management
- Timeout and retry support

**Example use cases**:
- REST API calls
- File downloads
- Form submissions

---

### Social Media

**Facebook**: facebook-sdk
```bash
pip install facebook-sdk
```

**Instagram**: instagrapi
```bash
pip install instagrapi
```

**Note**: Official Instagram API has limited access; instagrapi is a private API client

**Twitter/X**: tweepy
```bash
pip install tweepy
```

---

### Google Services

**Google Sheets**: gspread
```bash
pip install gspread google-auth
```

**Use when**: Reading/writing Google Sheets

**Example**:
```python
import gspread
from google.oauth2.service_account import Credentials

gc = gspread.service_account(filename='credentials.json')
sh = gc.open("My Spreadsheet")
worksheet = sh.sheet1
data = worksheet.get_all_records()
```

---

**Gmail**: google-api-python-client
```bash
pip install google-api-python-client google-auth
```

---

## Data Validation

### Email Validation

**email-validator**
```bash
pip install email-validator
```

```python
from email_validator import validate_email, EmailNotValidError

try:
    valid = validate_email('user@example.com')
    email = valid.email  # Normalized form
except EmailNotValidError as e:
    print(str(e))
```

---

### Phone Number Validation

**phonenumbers**
```bash
pip install phonenumbers
```

```python
import phonenumbers

number = phonenumbers.parse("+821012345678", None)
is_valid = phonenumbers.is_valid_number(number)
formatted = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
```

---

## Web Scraping

### BeautifulSoup (HTML parsing)
```bash
pip install beautifulsoup4 requests
```

**Use when**: Extracting data from HTML pages

```python
import requests
from bs4 import BeautifulSoup

response = requests.get('https://example.com')
soup = BeautifulSoup(response.content, 'html.parser')

# Find elements
title = soup.find('h1').text
links = soup.find_all('a')
```

---

### Selenium (Browser automation)
```bash
pip install selenium
```

**Use when**: Need to interact with JavaScript-heavy sites, fill forms, click buttons

**Note**: Requires browser driver (ChromeDriver, etc.)

---

## Email

### Send Email (SMTP)

**smtplib** (Built-in, but use with email.mime)

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg['From'] = 'sender@example.com'
msg['To'] = 'recipient@example.com'
msg['Subject'] = 'Report Ready'

body = 'Your daily report is attached.'
msg.attach(MIMEText(body, 'plain'))

# Send
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('sender@example.com', 'password')
server.send_message(msg)
server.quit()
```

---

### Send Email with Attachments

**Use email.mime.application for attachments**

```python
from email.mime.application import MIMEApplication

# Attach file
with open('report.xlsx', 'rb') as f:
    attach = MIMEApplication(f.read(), _subtype='xlsx')
    attach.add_header('Content-Disposition', 'attachment', filename='report.xlsx')
    msg.attach(attach)
```

---

## Database

### SQLite (Built-in)

```python
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')

# Insert
cursor.execute('INSERT INTO customers (name, email) VALUES (?, ?)', ('Alice', 'alice@example.com'))
conn.commit()

# Query
cursor.execute('SELECT * FROM customers')
rows = cursor.fetchall()

conn.close()
```

---

### PostgreSQL / MySQL

**psycopg2** (PostgreSQL)
```bash
pip install psycopg2-binary
```

**pymysql** (MySQL)
```bash
pip install pymysql
```

---

## Scheduling

### schedule (Simple scheduling)
```bash
pip install schedule
```

**Use when**: Running tasks on a schedule within Python

```python
import schedule
import time

def job():
    print("Running report...")

# Every day at 9am
schedule.every().day.at("09:00").do(job)

# Every hour
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

**Note**: For production, use OS-level schedulers (cron on Linux/macOS, Task Scheduler on Windows)

---

## Environment Variables

### python-dotenv
```bash
pip install python-dotenv
```

**Use when**: Loading API keys and secrets from .env files

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
```

**.env file**:
```
API_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
```

---

## Logging

**logging** (Built-in)

Already covered in common-patterns.md

---

## Configuration

### YAML Config Files

**PyYAML**
```bash
pip install pyyaml
```

```python
import yaml

# Read YAML
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print(config['database']['host'])
```

**config.yaml**:
```yaml
database:
  host: localhost
  port: 5432
  name: mydb

api:
  facebook_key: xxx
  instagram_key: yyy
```

---

### JSON Config Files

**json** (Built-in)

```python
import json

with open('config.json', 'r') as f:
    config = json.load(f)

print(config['api_key'])
```

---

## Testing

### pytest
```bash
pip install pytest
```

Already covered in tdd-guide.md

---

## Progress Bars

### tqdm
```bash
pip install tqdm
```

Already covered in common-patterns.md

---

## Date/Time

### arrow (Human-friendly dates)
```bash
pip install arrow
```

```python
import arrow

now = arrow.now()
print(now.humanize())  # "just now"

past = arrow.now().shift(days=-7)
print(past.humanize())  # "7 days ago"

# Parse and format
d = arrow.get('2025-10-26')
print(d.format('YYYY년 MM월 DD일'))  # "2025년 10월 26일"
```

**Alternative**: Built-in datetime is usually sufficient

---

## Recommendations by Domain

### Marketing (Social Media Reporting)

Required:
- `requests` - API calls
- `openpyxl` - Excel reports
- `python-dotenv` - API keys
- `pytest` - Testing

Optional:
- `facebook-sdk` - Facebook API
- `instagrapi` - Instagram API
- `pandas` - Data aggregation
- `tqdm` - Progress indication

---

### Finance (Expense Tracking, Reconciliation)

Required:
- `openpyxl` or `pandas` - Excel files
- `pdfplumber` - Extract data from receipts
- `pytest` - Testing

Optional:
- `PyYAML` - Config files (categories)
- `python-dotenv` - Credentials

---

### Sales (CRM Integration, Reports)

Required:
- `requests` - CRM API calls
- `openpyxl` or `pandas` - Reports
- `python-dotenv` - API credentials
- `pytest` - Testing

Optional:
- `smtplib` + `email` - Email reports
- `schedule` - Automated runs

---

### HR (Onboarding, Inventory)

Required:
- `requests` - API calls (Slack, email, etc.)
- `openpyxl` - Inventory tracking
- `python-dotenv` - Credentials
- `pytest` - Testing

Optional:
- `PyYAML` - Config files (employee templates)
- `smtplib` + `email` - Welcome emails

---

### Data Processing (File Merging, Transformation)

Required:
- `pandas` - Data manipulation
- `openpyxl` - Excel I/O
- `pytest` - Testing

Optional:
- `pdfplumber` - PDF extraction
- `beautifulsoup4` - Web scraping
- `sqlite3` (built-in) - Data storage

---

## Installation Best Practices

### requirements.txt

After implementing, create `requirements.txt`:

```bash
pip freeze > requirements.txt
```

**Or manually create**:
```
# requirements.txt
requests==2.31.0
openpyxl==3.1.2
python-dotenv==1.0.0
pytest==7.4.0
```

**Install dependencies**:
```bash
pip install -r requirements.txt
```

---

### Virtual Environment

Always use virtual environment:

```bash
# Create
python -m venv venv

# Activate
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install packages
pip install requests openpyxl pytest

# Deactivate
deactivate
```

---

## Summary Cheat Sheet

| Domain | Core Libraries |
|--------|----------------|
| **File I/O** | openpyxl, pandas, csv, pdfplumber |
| **HTTP/APIs** | requests, facebook-sdk, instagrapi, tweepy |
| **Google** | gspread, google-api-python-client |
| **Email** | smtplib (built-in), email.mime |
| **Database** | sqlite3 (built-in), psycopg2, pymysql |
| **Config** | python-dotenv, PyYAML, json (built-in) |
| **Testing** | pytest |
| **Scheduling** | schedule, cron (OS-level) |
| **Progress** | tqdm |
| **Validation** | email-validator, phonenumbers |
| **Web Scraping** | beautifulsoup4, selenium |
| **Date/Time** | datetime (built-in), arrow |

---

**General rule**: Start with built-in libraries, add third-party only when needed.
