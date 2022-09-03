# Library Management Database

This repo serves as a presentation demo for my end of semester Data Structures & Algorithms class Project. All future commits will only contain the relevant additions to scale this to a working GUI application. If you want to contribute to that, make a pull request, and let's create magic.

### Structure of the project

```bash

.
├── books.json
├── library.db
├── manager
│   ├── database
│   │   ├── core.py
│   │   ├── crud
│   │   │   ├── author.py
│   │   │   ├── book.py
│   │   │   ├── borrowed_book.py
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── schemas
│   │       ├── author.py
│   │       ├── book.py
│   │       ├── __init__.py
│   │       ├── library.py
│   │       └── users.py
│   ├── __init__.py
│   ├── main.py
│   ├── security.py
│   └── utils
│       ├── book_metadata_parser.py
│       └── __init__.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── requirements.txt
└── tests
    ├── conftest.py
    ├── crud
    │   ├── __init__.py
    │   ├── test_author.py
    │   ├── test_book.py
    │   ├── test_borrowed_book.py
    │   └── test_load_book_metadata.py
    └── __init__.py

7 directories, 31 files

```

# Quick Start

- Clone the repository

    ```bash
    git clone https://github.com/blackprince001/dsa-library-management
    ```

- Move into the directory

    ```bash
    cd dsa-library-management
    ```

- Set up a virtual environment with [Pipenv](https://pipenv.pypa.io/en/latest/index.html) and install the project dependencies (from the `Pipfile.lock` file to ensure deterministic builds)

  ```bash
  pipenv sync
  ```

- If you get `ModuleNotFoundError: No module named 'manager'`, you need to inject the package into `PYTHONPATH`.
One of the ways to so is to put the following code at the very beginning of `manager/main.py`

  ```python
  import sys
  from pathlib import Path
  
  sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
  ```

- For the lazy ones like me do not have pipenv install, just use the requirements.txt and download the dependencies to your path package path.
  
  ```bash
    python -m pip install -r requirements.txt
  ```

  while you're in `/dsa-library-management`

### Testing

To run the tests in the project:

- You need to install the dev packages:

  ```bash
  pipenv sync --dev
  ```
  
- Run pytest

  ```bash
  pipenv run pytest
  ```
