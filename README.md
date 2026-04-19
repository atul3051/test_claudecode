# add_two_numbers

A production-ready Python utility for adding two numeric values. Designed to be used both as an importable library and as a standalone command-line tool.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [As a CLI tool](#as-a-cli-tool)
  - [As a library](#as-a-library)
- [Input Validation](#input-validation)
- [Logging](#logging)
- [Running Tests](#running-tests)
- [CI/CD](#cicd)
- [Error Handling](#error-handling)

---

## Overview

This project provides a simple, well-tested, and production-hardened function to add two numbers. It demonstrates production engineering practices including:

- Type hints and docstrings
- Input validation with clear error messages
- Structured logging
- CLI interface via `argparse`
- Comprehensive unit tests with `pytest`
- Automated CI via GitHub Actions

---

## Features

| Feature | Details |
|---|---|
| Type hints | `add(a: float, b: float) -> float` |
| Input validation | Rejects non-numeric types, `NaN`, and `±inf` |
| Structured logging | ISO 8601 timestamps, named logger, INFO level by default |
| CLI interface | `--a` and `--b` flags, `--help`, exits with code 1 on error |
| Unit tests | 22 pytest tests covering happy path, edge cases, and invalid inputs |
| CI pipeline | GitHub Actions — runs on Python 3.9, 3.10, 3.11, 3.12 |

---

## Project Structure

```
.
├── add_two_numbers.py          # Core module: add() function + CLI entry point
├── test_add_two_numbers.py     # pytest unit tests (22 tests)
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── .gitignore                  # Excludes __pycache__, .pyc, .pytest_cache, etc.
└── README.md                   # This file
```

---

## Requirements

- Python 3.9 or later
- `pytest` (for running tests only)

No third-party runtime dependencies — the core module uses only the Python standard library (`argparse`, `logging`, `math`, `sys`).

---

## Installation

Clone the repository and install the test dependency:

```bash
git clone https://github.com/atul3051/test_claudecode.git
cd test_claudecode
pip install pytest
```

---

## Usage

### As a CLI tool

Pass two numbers using the `--a` and `--b` flags:

```bash
python add_two_numbers.py --a 5.5 --b 3.2
# 2024-01-01T12:00:00 [INFO] add(5.5, 3.2) = 8.7
# Result: 8.7
```

```bash
python add_two_numbers.py --a 10 --b -4
# Result: 6.0
```

Get help:

```bash
python add_two_numbers.py --help
```

Output:
```
usage: add_two_numbers [-h] --a A --b B

Add two numbers and print the result.

options:
  -h, --help  show this help message and exit
  --a A       First number (int or float)
  --b B       Second number (int or float)

Example: python add_two_numbers.py --a 5.5 --b 3.2
```

### As a library

Import and call `add()` directly in your own code:

```python
from add_two_numbers import add

result = add(3, 4.5)
print(result)  # 7.5

result = add(-10, 10)
print(result)  # 0
```

---

## Input Validation

The `add()` function validates inputs before performing arithmetic:

| Condition | Exception raised | Example |
|---|---|---|
| Non-numeric type | `TypeError` | `add("5", 3)` |
| `None` value | `TypeError` | `add(None, 3)` |
| `NaN` value | `ValueError` | `add(float('nan'), 3)` |
| Infinite value | `ValueError` | `add(float('inf'), 3)` |

```python
from add_two_numbers import add

add("hello", 3)    # TypeError: Both arguments must be int or float. Got: a=str, b=int
add(float('nan'), 1)  # ValueError: Arguments must not be NaN.
add(float('inf'), 1)  # ValueError: Arguments must be finite numbers, not infinity.
```

---

## Logging

The module uses Python's built-in `logging` library. Every successful call logs at `INFO` level:

```
2024-01-01T12:00:00 [INFO] add(5.5, 3.2) = 8.7
```

To change the log level in your own application:

```python
import logging
logging.getLogger("add_two_numbers").setLevel(logging.WARNING)
```

---

## Running Tests

Run the full test suite with:

```bash
pytest test_add_two_numbers.py -v
```

Expected output:

```
collected 22 items

test_add_two_numbers.py::TestAddHappyPath::test_two_positive_integers PASSED
test_add_two_numbers.py::TestAddHappyPath::test_two_positive_floats PASSED
test_add_two_numbers.py::TestAddHappyPath::test_positive_and_negative PASSED
test_add_two_numbers.py::TestAddHappyPath::test_two_negative_numbers PASSED
test_add_two_numbers.py::TestAddHappyPath::test_zeros PASSED
test_add_two_numbers.py::TestAddHappyPath::test_integer_and_float_mixed PASSED
test_add_two_numbers.py::TestAddHappyPath::test_large_numbers PASSED
test_add_two_numbers.py::TestAddHappyPath::test_negative_result PASSED
test_add_two_numbers.py::TestAddHappyPath::test_result_is_float_type PASSED
test_add_two_numbers.py::TestAddEdgeCases::test_very_small_floats PASSED
test_add_two_numbers.py::TestAddEdgeCases::test_very_large_floats PASSED
test_add_two_numbers.py::TestAddEdgeCases::test_add_zero_identity PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_string_input_first_arg PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_string_input_second_arg PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_none_input PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_list_input PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_nan_first_arg PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_nan_second_arg PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_inf_first_arg PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_negative_inf_second_arg PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_both_nan PASSED
test_add_two_numbers.py::TestAddInvalidInputs::test_error_message_contains_types PASSED

22 passed in 0.05s
```

### Test coverage breakdown

| Class | Tests | What it covers |
|---|---|---|
| `TestAddHappyPath` | 9 | Positive, negative, zero, floats, large numbers |
| `TestAddEdgeCases` | 3 | Very small/large floats, zero-identity property |
| `TestAddInvalidInputs` | 10 | Strings, None, lists, NaN, ±inf, error messages |

---

## CI/CD

GitHub Actions automatically runs the test suite on every push and pull request to `main` and `claude/*` branches.

**Workflow:** `.github/workflows/ci.yml`

| Step | Description |
|---|---|
| Checkout | Clones the repository |
| Set up Python | Installs Python 3.9, 3.10, 3.11, 3.12 (in parallel) |
| Install dependencies | `pip install pytest` |
| Run pytest | Full suite with verbose output |
| CLI smoke test | `python add_two_numbers.py --a 5 --b 3` |

---

## Error Handling

The CLI exits with code `1` on any validation error, making it safe to use in shell scripts:

```bash
python add_two_numbers.py --a hello --b 3
# 2024-01-01T12:00:00 [ERROR] Invalid input: Both arguments must be int or float...
echo $?  # 1
```

Successful execution exits with code `0`:

```bash
python add_two_numbers.py --a 5 --b 3
echo $?  # 0
```
