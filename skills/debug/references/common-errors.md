# Common Python Errors and Solutions

Quick reference for frequently encountered errors in Python automation tools.

## File and Path Errors

### FileNotFoundError
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/input.csv'
```

**Cause**: File doesn't exist at the specified path.

**Solutions**:
1. Check if file exists: `ls data/input.csv`
2. Create directory: `mkdir -p data`
3. Use absolute path:
   ```python
   from pathlib import Path
   file_path = Path(__file__).parent / "data" / "input.csv"
   ```
4. Check current working directory: `print(os.getcwd())`

---

### PermissionError
```
PermissionError: [Errno 13] Permission denied: 'output.xlsx'
```

**Cause**: Don't have permission to read/write file.

**Solutions**:
1. Check if file is open in another program (Excel, etc.)
2. Close file and try again
3. Check file permissions: `ls -l output.xlsx`
4. Run with appropriate permissions

---

## Import and Package Errors

### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'openpyxl'
```

**Cause**: Python package not installed.

**Solutions**:
1. Install package: `pip install openpyxl`
2. Check virtual environment is activated: `which python`
3. Add to requirements.txt:
   ```
   openpyxl==3.1.2
   ```

---

### ImportError
```
ImportError: cannot import name 'FacebookClient' from 'src.facebook_client'
```

**Cause**: Class/function doesn't exist in the module.

**Solutions**:
1. Check spelling: `FacebookClient` vs `FacebookClient`
2. Check if class is defined in that file
3. Check if file has syntax errors (prevents import)

---

## Type Errors

### AttributeError (NoneType)
```
AttributeError: 'NoneType' object has no attribute 'get'
```

**Cause**: Variable is `None` when code expected an object.

**Solutions**:
1. Check if function returned `None`:
   ```python
   result = some_function()
   print(f"Result: {result}")  # Is it None?
   ```
2. Add None check:
   ```python
   if result is None:
       print("Error: No data returned")
       return
   ```
3. Find why function returned `None` instead of expected value

---

### TypeError (Operand)
```
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Cause**: Trying to combine incompatible types.

**Solutions**:
1. Convert to same type:
   ```python
   # Bad
   total = 100 + "50"

   # Good
   total = 100 + int("50")
   # or
   total = str(100) + "50"
   ```
2. Check variable types:
   ```python
   print(type(value))  # <class 'str'> or <class 'int'>?
   ```

---

### TypeError (Argument)
```
TypeError: fetch_data() takes 1 positional argument but 2 were given
```

**Cause**: Calling function with wrong number of arguments.

**Solutions**:
1. Check function signature:
   ```python
   def fetch_data(page_id):  # Takes 1 argument
   ```
2. Call with correct arguments:
   ```python
   fetch_data("my_page")  # 1 argument ✓
   ```

---

## Dictionary and Data Errors

### KeyError
```
KeyError: 'likes'
```

**Cause**: Dictionary key doesn't exist.

**Solutions**:
1. Check what keys exist:
   ```python
   print(data.keys())  # dict_keys(['comments', 'shares'])
   ```
2. Use `.get()` with default:
   ```python
   # Bad - crashes if 'likes' missing
   likes = data['likes']

   # Good - returns 0 if 'likes' missing
   likes = data.get('likes', 0)
   ```
3. Check for key before accessing:
   ```python
   if 'likes' in data:
       likes = data['likes']
   ```

---

### IndexError
```
IndexError: list index out of range
```

**Cause**: Trying to access index that doesn't exist in list.

**Solutions**:
1. Check list length:
   ```python
   print(f"List length: {len(my_list)}")
   ```
2. Use safe access:
   ```python
   # Bad
   first = my_list[0]  # Crashes if list is empty

   # Good
   first = my_list[0] if my_list else None
   ```

---

## Value Errors

### ValueError (Invalid Literal)
```
ValueError: invalid literal for int() with base 10: 'abc'
```

**Cause**: Trying to convert invalid string to number.

**Solutions**:
1. Validate before converting:
   ```python
   if value.isdigit():
       num = int(value)
   else:
       print(f"Invalid number: {value}")
   ```
2. Use try-except:
   ```python
   try:
       num = int(value)
   except ValueError:
       print(f"Cannot convert '{value}' to number")
       num = 0  # Default value
   ```

---

### ValueError (JSON Decode)
```
ValueError: Expecting value: line 1 column 1 (char 0)
```

**Cause**: Invalid JSON string.

**Solutions**:
1. Check if response is actually JSON:
   ```python
   print(response.text)  # Is it JSON or HTML error page?
   ```
2. Check API response status:
   ```python
   if response.status_code != 200:
       print(f"API error: {response.status_code}")
       print(response.text)
   ```
3. Use try-except:
   ```python
   try:
       data = response.json()
   except ValueError:
       print("Invalid JSON response")
       print(response.text)
   ```

---

## API and Network Errors

### requests.exceptions.ConnectionError
```
ConnectionError: Failed to establish a new connection
```

**Cause**: Cannot connect to API (network issue, wrong URL, API down).

**Solutions**:
1. Check internet connection
2. Verify API URL is correct
3. Check if API is down (try in browser)
4. Add retry logic:
   ```python
   import time
   for attempt in range(3):
       try:
           response = requests.get(url)
           break
       except ConnectionError:
           if attempt < 2:
               time.sleep(2)
               continue
           raise
   ```

---

### requests.exceptions.Timeout
```
ReadTimeout: HTTPSConnectionPool: Read timed out
```

**Cause**: Request took too long.

**Solutions**:
1. Increase timeout:
   ```python
   response = requests.get(url, timeout=30)  # 30 seconds
   ```
2. Check if API is slow/down
3. Add retry with exponential backoff

---

### HTTP 401 Unauthorized
```
Response: 401 Unauthorized
```

**Cause**: Invalid API credentials.

**Solutions**:
1. Check .env file has correct API key
2. Verify API key is not expired
3. Check API key has correct permissions
4. Test API key in API console/docs

---

### HTTP 429 Too Many Requests
```
Response: 429 Too Many Requests
```

**Cause**: Hit API rate limit.

**Solutions**:
1. Add delay between requests:
   ```python
   import time
   time.sleep(1)  # Wait 1 second
   ```
2. Implement exponential backoff
3. Check API rate limits in documentation
4. Cache responses to reduce requests

---

## Excel/CSV Errors

### openpyxl: InvalidFileException
```
InvalidFileException: openpyxl does not support the old .xls file format
```

**Cause**: Trying to open old Excel format (.xls) with openpyxl.

**Solutions**:
1. Convert file to .xlsx format
2. Use pandas instead:
   ```python
   import pandas as pd
   df = pd.read_excel('file.xls')  # Handles both .xls and .xlsx
   ```

---

### csv.Error: line contains NUL
```
csv.Error: line contains NULL byte
```

**Cause**: CSV file is corrupted or has binary data.

**Solutions**:
1. Open file in text editor to check contents
2. Re-export CSV from source
3. Skip bad lines:
   ```python
   with open('file.csv', 'r', errors='ignore') as f:
       reader = csv.reader(f)
   ```

---

## Environment Variable Errors

### KeyError (os.getenv)
```
KeyError: 'API_KEY'
```

**Cause**: Environment variable not set or .env file not loaded.

**Solutions**:
1. Check .env file exists
2. Load .env file:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
3. Use default value:
   ```python
   api_key = os.getenv('API_KEY', 'default_key')
   ```
4. Validate at startup:
   ```python
   api_key = os.getenv('API_KEY')
   if not api_key:
       raise ValueError("API_KEY not set in .env file")
   ```

---

## Encoding Errors

### UnicodeDecodeError
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff
```

**Cause**: File has different encoding than expected.

**Solutions**:
1. Try different encoding:
   ```python
   # Common encodings
   with open('file.txt', 'r', encoding='cp949') as f:  # Korean
   with open('file.txt', 'r', encoding='latin-1') as f:
   ```
2. Ignore errors:
   ```python
   with open('file.txt', 'r', encoding='utf-8', errors='ignore') as f:
   ```

---

## Quick Troubleshooting Checklist

**For any error**:
1. Read the error message carefully (last line + traceback)
2. Note the file and line number
3. Add print statements to see variable values
4. Check types: `print(type(variable))`
5. Check if None: `print(variable is None)`
6. Google the exact error message

**For API errors**:
1. Check internet connection
2. Verify API credentials in .env
3. Test API endpoint in browser/Postman
4. Check API documentation for changes
5. Look at response status code and body

**For file errors**:
1. Check if file exists: `ls path/to/file`
2. Check current directory: `pwd`
3. Use absolute paths
4. Check file is not open in another program
5. Check file permissions

**For package errors**:
1. Check virtual environment is activated
2. Install missing package: `pip install package-name`
3. Check requirements.txt is up to date
4. Try `pip list` to see what's installed
