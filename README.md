# Automated API Testing Project - The Movie Database API 🎬

## Project Overview

This project implements a comprehensive automated testing framework for validating **The Movie Database (TMDB)** public REST API. The system runs Python-based tests, generates detailed reports, and creates visual dashboards of test results. The project demonstrates modern API testing best practices, CI/CD integration, and automated reporting capabilities.

This project contains 20 different test cases covering functional, negative, boundary value, and performance testing of the API.

## Key Features

### 🔧 API Testing Capabilities
- **Functional tests**: Validation of basic API operations (GET, POST queries)
- **Negative tests**: Error handling and validation testing (invalid API key, invalid parameters)
- **Boundary Value Analysis (BVA)**: 2-point Boundary tests for page parameters
- **Non-functional tests**: Performance and data integrity validation

### 📊 Reporting and Visualization
- **Automatic JSON reports**: Structured test results for machine processing
- **pytest HTML reports**: Detailed test documentation
- **Custom dashboard**: Modern, interactive HTML dashboard with Jinja2 templates

### 🚀 CI/CD Integration
- **GitHub Actions workflow**: Automatic testing on every push and pull request
- **Artifact management**: 30-day retention of test reports
- **Manual execution**: workflow_dispatch support
- **GitHub Summary**: Instant test result display

### 🏗️ Modular Architecture
- Clean code structure
- Reusable API functions
- Easily extensible test cases
- Environment-based configuration (.env)

## Technology Stack

| Technology | Usage |
|------------|-------|
| **Python** | Main programming language |
| **pytest** | Testing framework |
| **requests** | HTTP client library |
| **python-dotenv** | Environment variable management |
| **Jinja2** | HTML template engine |
| **pytest-json-report** | JSON report generation |
| **pytest-html** | HTML report generation |
| **GitHub Actions** | CI/CD pipeline |

## Installation and Setup

### Prerequisites

- **Python 3.13+** installed
- **Git** version control
- **TMDB API key** (free registration required: [TMDB API](https://www.themoviedb.org/settings/api))

### 1. Clone the Repository

```bash
git clone https://github.com/csokanandor95/api-testing-project.git
cd api-testing-project
```

### 2. Create Python Virtual Environment (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `src/` directory:

```bash
cd src
cp .env.example .env  # If example file exists, otherwise:
```

Edit the `.env` file and add your TMDB API key:

```env
TMDB_API_KEY=your_actual_api_key_here
```

**IMPORTANT:** The `.env` file is included in `.gitignore` and will not be version controlled (for security reasons).

## Usage

### Running Tests Locally

#### Simple Execution with run_tests.py

```bash
cd src
python run_tests.py
```

This command will:
1. Run all test cases
2. Generate JSON and HTML reports (with timestamp)
3. Create a custom dashboard
4. Summarize the results

#### Manual pytest Execution

```bash
cd src
pytest test_cases.py -v
```

Additional pytest options:

```bash
# Run a specific test only
pytest test_cases.py::test_tc01_popular_movies -v

# Detailed output
pytest test_cases.py -v -s

# Generate HTML report
pytest test_cases.py --html=report.html --self-contained-html

# Generate JSON report
pytest test_cases.py --json-report --json-report-file=report.json
```

### Dashboard Generation

The dashboard is automatically generated when running `run_tests.py`. It can also be created manually:

```bash
cd src
python report_generator.py
```

Opening the generated dashboard:
```bash
# Open the latest dashboard in browser
# Windows
start ../dashboard/dashboard_YYYYMMDD_HHMMSS.html

# Linux/Mac
open ../dashboard/dashboard_YYYYMMDD_HHMMSS.html
```

### CI/CD - GitHub Actions

The project automatically runs tests on every `push` and `pull request` to all branches.

#### Manual Execution on GitHub

1. Go to the repository's **Actions** tab
2. Select the **API Tests CI/CD** workflow
3. Click the **Run workflow** button
4. Select the branch and click **Run workflow**

#### Viewing Test Results

- Download reports from the **Artifacts** section
- View summary statistics in the **Summary** tab
- Detailed logs are available for every step in the workflow

## Test Cases Overview

### Functional Tests (TC01-TC06)

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC01 | Get popular movies | 200 OK, non-empty results array |
| TC02 | Movie details with valid ID | 200 OK, correct movie data |
| TC03 | Search movie with valid query | 200 OK, relevant results |
| TC04 | Get movie genres list | 200 OK, genres array |
| TC05 | Popular movies page 2 | 200 OK, page=2 |
| TC06 | Hungarian language parameter | 200 OK |

### Negative Tests (TC07-TC12)

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC07 | Invalid API key | 401 Unauthorized |
| TC08 | Missing API key | 401 Unauthorized |
| TC09 | Invalid movie ID (-1) | 400/404 |
| TC10 | Nonsense search query | 200 OK, empty results |
| TC11 | 300 character search query | 200 OK |
| TC12 | Empty search string | 200 OK, empty results |

### Boundary Value Analysis (TC13-TC16)

100% boundary value coverage on the `page` parameter (Min: 1, Max: 500)

| Test ID | Description | Value | Expected Result |
|---------|-------------|-------|-----------------|
| TC13 | Lower bound - invalid | page=0 | 400 Bad Request |
| TC14 | Lower bound - valid | page=1 | 200 OK |
| TC15 | Upper bound - valid | page=500 | 200 OK |
| TC16 | Upper bound - invalid | page=501 | 400 Bad Request |

### Non-functional Tests (TC17-TC20)

| Test ID | Category | Description | Expected Result |
|---------|----------|-------------|-----------------|
| TC17 | Performance | Response time | < 2 seconds |
| TC18 | Performance | Response size | < 1 MB |
| TC19 | Data integrity | JSON structure | Correct keys and types |
| TC20 | Data integrity | Data types | Validate int, str types |

## Report Examples

### pytest HTML Report

pytest automatically generates a detailed HTML report for every test run:
- Summary statistics
- Detailed test case descriptions
- Errors and stack traces
- Execution times

### Custom Dashboard

The custom dashboard provides a modern, interactive interface:
- **Statistics cards**: Summary (total, passed, failed, skipped, duration, success rate)
- **Progress bar**: Visual success rate
- **Detailed test list**: Status, execution time, and errors for each test
- **Responsive design**: Mobile and desktop support

## License

This project serves educational/learning purposes and uses The Movie Database (TMDB) API.

**Important notes:**
- TMDB API usage requires registration: https://www.themoviedb.org/settings/api
- TMDB trademarks and data are property of The Movie Database
- This project is unofficial and not affiliated with TMDB

## Contact and Contribution

### Author
- **GitHub:** [@csokanandor95](https://github.com/csokanandor95)

### Bug Reports

If you find a bug or have suggestions, please open a [GitHub Issue](https://github.com/csokanandor95/api-testing-project/issues)!

---

**🎯 Made during early morning or late night hours** fueled by lots of coffee! ☕ Because I love coding and software QA.

---