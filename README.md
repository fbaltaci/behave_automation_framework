# Behave API Automation Framework

This is a Python-based API test automation framework using [Behave](https://behave.readthedocs.io/en/stable/), built for
validating the [ToolsQA BookStore API](https://bookstore.toolsqa.com/).

## Getting Started

## Project Structure

```
behave_automation_framework/
├── features/
│   ├── login.feature              # Login test scenarios (Gherkin)
│   ├── steps/
│   │   └── login_steps.py         # Step definitions for login
│   └── environment.py             # Setup/teardown hooks
|── logs/
│   └── test_log_20240205_103000.log  # Log file
|── reports/
|   └── allure-report/
|       ├── index.html
|       └── ...
|   └── allure-results/
├── utils/
│   ├── api_helper.py              # API request helper functions
│   ├── date_utils.py              # Timestamp generation
│   └── user_utils.py              # Dynamic user utilities
├── .env                           # Environment variables (e.g. base URL)
├── .env.template                  # Template for environment config
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # Documentation
```

### 1. Clone the repository

```
git clone https://github.com/fbaltaci/behave_automation_framework.git
cd behave_automation_framework
```

### 2. Create and activate a virtual environment

```
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Set up environment variables

Update .env or copy from .env.template:

```
BASE_URL=https://bookstore.toolsqa.com
```

### 5. Run tests

To run all scenarios:

```bash
behave
```

To run specific feature file:

```bash
behave features/login.feature
```

To run specific scenario:

```bash
behave -n "Successfully create a new user with valid credentials"
```

To run tagged scenarios:

```bash
behave -t @login
```

## Allure Reporting Integration

This framework supports [Allure](https://allurereport.org/docs/) for advanced and interactive test reporting.

### Install Allure CLI

Allure must be installed separately from Python packages.

#### On Windows (Recommended via Scoop):

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
scoop install allure
```

Verify Installation

```powershell
allure --version
```

Alternatively, you can download [Allure](https://github.com/allure-framework/allure2/releases) manually and add it to
your system PATH.

### Generate Allure Results

Run Behave tests with the Allure formatter:

```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

### Generate and Open HTML Report

```bash
allure generate allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

This will open a browser window with a detailed test report.

### Required Python Package

Make sure allure-behave is installed:

```bash
pip install allure-behave
```

## Built With

- [Behave](https://behave.readthedocs.io/en/stable/) - BDD testing framework
- [Requests](https://docs.python-requests.org/en/latest/) - HTTP library
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable loader
- [Allure](https://allurereport.org/docs/) - Test reporting framework
- [Allure Behave](https://github.com/allure-framework/allure-python/tree/master/allure-behave) - Allure integration for
  Behave
