# Behave API Automation Framework

This is a Python-based API test automation framework using [Behave](https://behave.readthedocs.io/en/stable/), built for
validating the [ToolsQA BookStore API](https://bookstore.toolsqa.com/).. It is designed with modularity and clarity in
mind, and
ideal for portfolio demonstrations or scalable automation suites.

## Getting Started

## 📁 Project Structure

```
behave_automation_framework/
├── features/
│   ├── login.feature              # Login test scenarios (Gherkin)
│   ├── steps/
│   │   └── login_steps.py         # Step definitions for login
│   └── environment.py             # Setup/teardown hooks
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

## Built With

- [Behave](https://behave.readthedocs.io/en/stable/) - BDD testing framework
- [Requests](https://docs.python-requests.org/en/latest/) - HTTP library
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable loader
