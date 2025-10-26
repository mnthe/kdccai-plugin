# Scenario Examples by Domain

This file provides concrete scenario examples across different work domains to inspire and guide planning.

## Marketing

### Example 1: Social Media Report Automation

**SCN-001: Daily engagement report from multiple platforms**

Description: Marketing manager needs daily summary of engagement metrics from Facebook, Instagram, and Twitter

Input:
- Social media accounts configured in config.json
- Date range: last 24 hours
- API credentials in .env

Expected Output:
- Excel file: reports/social-engagement-YYYY-MM-DD.xlsx
- Summary sheet with total metrics
- Detail sheets for each platform
- Engagement trends chart

Steps:
1. User runs: `python src/social_report.py`
2. Tool authenticates with each platform API
3. Tool fetches likes, comments, shares, reach for last 24 hours
4. Tool calculates total engagement score
5. Tool generates Excel with charts
6. Tool saves to reports/ directory

---

### Example 2: Campaign Performance Tracker

**SCN-002: Weekly ad campaign performance comparison**

Description: Compare performance of 3 running ad campaigns weekly

Input:
- Campaign IDs in campaigns.csv
- Date range: last 7 days
- Budget allocation data

Expected Output:
- PDF report: campaigns/weekly-report-YYYY-WW.pdf
- Cost per conversion for each campaign
- ROI calculation
- Recommendation for budget reallocation

Steps:
1. User runs: `python src/campaign_tracker.py --weekly`
2. Tool fetches ad performance from Facebook Ads Manager
3. Tool calculates CPC, CTR, conversion rate, ROI for each campaign
4. Tool compares against targets
5. Tool generates PDF with visualizations and recommendations
6. Tool emails report to stakeholders

---

## Finance

### Example 3: Monthly Expense Reconciliation

**SCN-001: Reconcile credit card transactions with receipts**

Description: Match credit card transactions with scanned receipts and flag discrepancies

Input:
- credit_card_export.csv (downloaded from bank)
- receipts/ folder with scanned receipt PDFs
- categories.yaml for expense categorization

Expected Output:
- reconciliation/YYYY-MM-reconciliation.xlsx
- Matched transactions (green)
- Unmatched transactions (red)
- Missing receipts list
- Category summary

Steps:
1. User downloads credit card statement CSV
2. User places receipts in receipts/ folder
3. User runs: `python src/reconcile.py --month 2025-10`
4. Tool parses credit card CSV
5. Tool extracts amounts from receipt PDFs using OCR
6. Tool matches transactions to receipts (fuzzy matching on date + amount)
7. Tool categorizes expenses using categories.yaml
8. Tool generates Excel with highlighted discrepancies

---

### Example 4: Budget vs Actual Variance Report

**SCN-002: Monthly budget variance analysis**

Description: Compare actual spending against budget and highlight variances > 10%

Input:
- budget.xlsx (annual budget by category)
- actual_expenses_YYYY-MM.csv (from accounting system)

Expected Output:
- variance/YYYY-MM-variance.pdf
- Table showing budget vs actual by category
- Variance percentage and amount
- Highlighted categories over 10% variance
- Cumulative YTD variance

Steps:
1. User exports actual expenses from accounting system
2. User runs: `python src/variance_report.py --month 10`
3. Tool loads budget from budget.xlsx
4. Tool loads actual from CSV
5. Tool calculates variance for each category
6. Tool highlights variances > 10%
7. Tool generates PDF with charts
8. Tool saves to variance/ directory

---

## Sales

### Example 5: Weekly Pipeline Report

**SCN-001: Sales pipeline snapshot for weekly review**

Description: Generate snapshot of sales pipeline showing deals by stage

Input:
- CRM export: opportunities_export.csv
- Date: current week
- Sales targets from targets.yaml

Expected Output:
- pipeline/weekly-YYYY-WW.pdf
- Deals by stage (funnel chart)
- Total pipeline value
- Forecasted close amount
- At-risk deals (no activity in 7 days)

Steps:
1. User exports opportunities from CRM
2. User runs: `python src/pipeline_report.py`
3. Tool parses opportunities CSV
4. Tool groups by stage
5. Tool calculates total value per stage
6. Tool identifies at-risk deals (last_activity > 7 days ago)
7. Tool generates funnel chart
8. Tool creates PDF report

---

### Example 6: Monthly Commission Calculator

**SCN-002: Calculate sales commissions based on closed deals**

Description: Calculate commissions for each sales rep based on deals closed this month

Input:
- closed_deals_YYYY-MM.csv (from CRM)
- commission_rules.yaml (tiered commission structure)
- sales_reps.csv (rep info and quotas)

Expected Output:
- commissions/YYYY-MM-commissions.xlsx
- Sheet per sales rep with deal list
- Commission amount per deal
- Total commission for the month
- Tier achieved (if tiered structure)

Steps:
1. User exports closed deals from CRM
2. User runs: `python src/commission_calc.py --month 10`
3. Tool loads commission rules from YAML
4. Tool groups deals by sales rep
5. Tool applies commission tiers based on total sales
6. Tool calculates commission per deal
7. Tool generates Excel with summary + detail sheets

---

## HR / Operations

### Example 7: New Employee Onboarding Automation

**SCN-001: Create accounts and send welcome package for new hire**

Description: Automate account creation across systems when new employee starts

Input:
- new_hire.yaml (name, email, department, start_date, manager)
- email_templates/ (welcome email templates)

Expected Output:
- Accounts created (email, Slack, project management tool)
- Welcome email sent with credentials and onboarding checklist
- Manager notified
- HR informed of completion
- Log entry in onboarding_log.csv

Steps:
1. HR fills new_hire.yaml with employee details
2. HR runs: `python src/onboard.py --file new_hire.yaml`
3. Tool creates email account via API
4. Tool creates Slack account and adds to department channel
5. Tool creates project management account
6. Tool generates temporary password
7. Tool sends welcome email with credentials
8. Tool notifies manager
9. Tool logs completion

---

### Example 8: Equipment Inventory Tracker

**SCN-002: Monthly equipment check and low-stock alert**

Description: Check equipment inventory and alert when items are below threshold

Input:
- inventory.xlsx (current inventory levels)
- thresholds.yaml (minimum levels per item)

Expected Output:
- inventory/YYYY-MM-status.pdf
- Current levels by item
- Items below threshold (red)
- Items near threshold (yellow)
- Recommended order quantities
- Email alert to procurement

Steps:
1. User runs: `python src/inventory_check.py`
2. Tool loads current inventory from Excel
3. Tool loads thresholds from YAML
4. Tool compares current vs threshold
5. Tool flags low-stock items
6. Tool calculates recommended order quantities
7. Tool generates PDF report
8. Tool emails procurement if any items below threshold

---

## Data Processing (General)

### Example 9: Multi-File Excel Merger

**SCN-001: Merge multiple Excel files into one master file**

Description: Combine monthly sales reports from different regions into annual report

Input:
- data/monthly/ folder with files: sales-YYYY-MM.xlsx
- Each file has same structure (columns: Date, Region, Product, Amount)

Expected Output:
- output/annual-sales-YYYY.xlsx
- All data combined into single sheet
- Sorted by date
- Duplicates removed
- Summary sheet with totals by region and month

Steps:
1. User places monthly files in data/monthly/
2. User runs: `python src/merge_excel.py --year 2025`
3. Tool finds all files matching sales-2025-*.xlsx
4. Tool reads each file
5. Tool validates column structure
6. Tool combines into single DataFrame
7. Tool removes duplicates based on (Date, Region, Product)
8. Tool creates summary pivot table
9. Tool writes to output/annual-sales-2025.xlsx

---

### Example 10: CSV to Database Import

**SCN-002: Import CSV data into SQLite database with validation**

Description: Import customer data from CSV, validate, and insert into database

Input:
- import/customers.csv
- Columns: CustomerID, Name, Email, Phone, Country
- Validation rules in validation_rules.yaml

Expected Output:
- Data inserted into customers.db
- import_log.txt with success/error counts
- errors.csv with rows that failed validation

Steps:
1. User places customers.csv in import/
2. User runs: `python src/import_customers.py`
3. Tool reads CSV
4. Tool validates each row:
   - CustomerID is unique
   - Email format is valid
   - Phone format matches country
5. Tool inserts valid rows into database
6. Tool writes invalid rows to errors.csv
7. Tool generates import_log.txt with statistics

---

## Pattern Recognition

Notice the common patterns:

**Input → Process → Output**:
- Input: CSV, Excel, API, config files
- Process: Parse, validate, transform, calculate
- Output: Excel, PDF, email, database, log

**Error Handling**:
- Validation before processing
- Error logs or error files
- Graceful degradation (partial success)

**Verification**:
- Specific file paths
- Expected content (rows, totals, flags)
- Notification confirmation

**User Experience**:
- Single command to run
- Clear output location
- Status/progress indication
- Error messages in user's language
