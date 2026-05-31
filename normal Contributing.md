# CONTRIBUTING.md – Contributing to ClinicEase

Thank you for your interest in contributing to **ClinicEase**! This document explains everything you need to get started as a contributor.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Coding Standards](#coding-standards)
- [How to Pick Issues](#how-to-pick-issues)
- [How to Submit a PR](#how-to-submit-a-pr)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)

---

## Prerequisites

Before contributing, make sure you have:

- **Python 3.12+** installed
- **Git** installed
- **pip** (Python package manager)
- A **GitHub account**
- Basic knowledge of Python, FastAPI, and pytest

---

## Setup Instructions

### 1. Fork the Repository

Click the **Fork** button at the top right of the repository page. This creates your own copy of ClinicEase.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/ClinicEase-Online-Doctor-Appointment-Booking-System.git
cd ClinicEase-Online-Doctor-Appointment-Booking-System
```

### 3. Install Dependencies

```bash
pip install bcrypt pytest pytest-cov fastapi uvicorn httpx pydantic
```

### 4. Verify Setup — Run All Tests

```bash
python -m pytest tests/ -v
```

You should see **188 tests passing**. If any fail, check that all files are in the correct folders.

### 5. Run the API Locally

```bash
uvicorn api.main:app --reload
```

Open **http://localhost:8000/docs** to see the Swagger UI.

---

## Coding Standards

### Python Style
- Follow **PEP 8** — 4 spaces for indentation, max line length 100 characters
- Use **type hints** on all function parameters and return types
- Write **docstrings** for all classes and public methods

### Testing Requirements
- Every new feature **must** include unit tests
- Every new API endpoint **must** include an integration test in `tests/test_api.py`
- Tests must pass before a PR can be merged
- Aim for **at least 80% code coverage** on new code

### File Naming
- All Python files must be **lowercase with underscores** (e.g., `patient_service.py`)
- Test files must start with `test_` (e.g., `test_patient_service.py`)

### Commit Messages
Use the conventional commit format:
```
feat: add medication refill alert endpoint
fix: correct slot double-booking race condition
docs: update README with new API endpoints
test: add tests for doctor availability search
```

---

## How to Pick Issues

1. Go to the **Issues** tab on the main repository
2. Filter by label:
   - `good-first-issue` — Simple tasks perfect for newcomers
   - `feature-request` — New features the project needs
   - `bug` — Something that is broken and needs fixing
3. Comment on the issue: **"I'd like to work on this"**
4. Wait for a maintainer to assign it to you before starting

### Good First Issues for Beginners
Look for issues tagged `good-first-issue` — these are small, well-defined tasks that do not require deep knowledge of the codebase.

---

## How to Submit a PR

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

Write your code and tests. Make sure all 188 existing tests still pass:

```bash
python -m pytest tests/ -v
```

### 3. Commit Your Changes

```bash
git add .
git commit -m "feat: describe what you did"
```

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Open a Pull Request

1. Go to the original repository on GitHub
2. Click **"Compare & pull request"**
3. Fill in the PR template:
   - **What does this PR do?**
   - **Which issue does it close?** (e.g., `Closes #5`)
   - **How was it tested?**
4. Click **Create pull request**

### 6. Wait for CI and Review

- The GitHub Actions CI pipeline will run automatically
- All 188 tests must pass before the PR can be merged
- A maintainer will review your code and may request changes
- Once approved, your PR will be merged! 🎉

---

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_services.py -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov=services --cov=api --cov-report=term-missing

# Run a single test
python -m pytest tests/test_all.py::TestUser::test_register_hashes_password -v
```

---

## Project Structure

```
ClinicEase/
├── src/                    # Core domain classes (User, Patient, Doctor, etc.)
├── services/               # Business logic layer
├── api/                    # FastAPI REST endpoints
├── repositories/           # Data persistence layer
├── factories/              # Repository factory for storage switching
├── creational_patterns/    # Design pattern implementations
├── tests/                  # All unit and integration tests
└── .github/workflows/      # CI/CD pipeline
```

---

## Need Help?

- Open a **GitHub Discussion** or comment on the relevant issue
- Read the full documentation in the repo's markdown files
- Check the [FastAPI docs](https://fastapi.tiangolo.com/) for API questions

We appreciate every contribution, big or small! 🙏

---

*ClinicEase — Cape Peninsula University of Technology | Software Engineering*