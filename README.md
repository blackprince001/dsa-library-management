# This is the Structure of the Project


```
.
├── app
│   ├── __init__.py
│   ├── library.py
│   └── session.py
├── assets
│   └── books.json
├── demo.ipynb
├── manager - My implementation
│   ├── database
│   │   ├── core.py
│   │   ├── crud - Create, Read, Update, Delete operations
│   │   │   ├── author.py
│   │   │   ├── book.py
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   ├── models.py - ORM Mapper Tables
│   │   └── schemas - Class representations of ORM tables
│   │       ├── author.py
│   │       ├── book.py
│   │       ├── library.py
│   │       └── users.py
│   ├── __init__.py
│   ├── main.py
│   └── security.py - Password hashing and verification
├── parser.py
├── Pipfile - Dependencies list
├── Pipfile.lock
├── README.md
├── test_json_file.py
├── tests
│   ├── conftest.py - Common fixtures
│   ├── crud
│   │   ├── __init__.py
│   │   ├── test_author.py
│   │   └── test_book.py
│   ├── __init__.py
└── test_session.py
```

# Quick Start
- Clone the repository
    ```
    git clone https://github.com/blackprince001/Library_Management
    ```

- Move into the directory
    ```
    cd Library_Management
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
