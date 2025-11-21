# How to Use the Virtual Environment

Your project has a virtual environment (`.venv`) that should be activated before running the backend.

## Option 1: Activate Virtual Environment (Recommended)

**Windows PowerShell:**
```powershell
cd C:\Users\rakes\Downloads\Plant_det
.\.venv\Scripts\Activate.ps1
cd backend
python backend.py
```

**Windows Command Prompt:**
```cmd
cd C:\Users\rakes\Downloads\Plant_det
.venv\Scripts\activate.bat
cd backend
python backend.py
```

## Option 2: Use Virtual Environment Python Directly

You can run the backend using the virtual environment's Python directly:

```powershell
cd C:\Users\rakes\Downloads\Plant_det\backend
..\..venv\Scripts\python.exe backend.py
```

## Option 3: Use the Batch File

The `start_system.bat` file has been updated to automatically use the virtual environment if it exists.

## Verify Virtual Environment

To check if you're using the virtual environment:
```python
import sys
print(sys.executable)
```

If it shows `.venv` in the path, you're using the virtual environment.

## Install Packages in Virtual Environment

When the virtual environment is activated:
```bash
pip install python-dotenv
```

Or use the virtual environment Python directly:
```bash
.venv\Scripts\python.exe -m pip install python-dotenv
```

