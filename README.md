# This is the Structure of the Project


```
.
├── assets
│   └── books.json
├── manager
│   ├── database
│   │   ├── core.py
│   │   ├── crud
│   │   │   ├── author.py
│   │   │   ├── book.py
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── schemas
│   │       ├── author.py
│   │       ├── book.py
│   │       ├── __init__.py
│   │       ├── library.py
│   │       └── users.py
│   ├── __init__.py
│   ├── main.py
│   └── security.py
├── Pipfile
├── Pipfile.lock
├── README.md
└── tests
    ├── conftest.py
    ├── crud
    │   ├── __init__.py
    │   ├── test_author.py
    │   └── test_book.py
    └── __init__.py

7 directories, 24 files


```

# Quick Start
- Clone the repository
    ```
    git clone https://github.com/blackprince001/dsa-library-management
    ```

- Move into the directory
    ```
    cd dsa-library-management
    ```

- Set up a virtual environment with [Pipenv](https://pipenv.pypa.io/en/latest/index.html) and install the project dependencies (from the `Pipfile.lock` file to ensure deterministic builds)
  ```
  pipenv sync
  ```

- If you get `ModuleNotFoundError: No module named 'manager'`, you need to inject the package into `PYTHONPATH`.
One of the ways to so is to put the following code at the very beginning of `manager/main.py`
  ```
  import sys
  from pathlib import Path
  
  sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
  ```


### Testing
To run the tests in the project:

- You need to install the dev packages:
  ```
  pipenv sync --dev
  ```
  
- Run pytest
  ```
  pipenv run pytest
  ```
