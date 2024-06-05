# Hoa

Extract data relevant for HOA property.

## Summary

Precommit must pass before commits will run.

- `hoa_property`: is the project module.  This will contain config, logging and any other project centric data.
- `extract`: this module deals with extracting data from files.  These can be text, image, binary or any other sort of data.
- `ocr`: this module deals with running ocr processes on files.

`load_hoa_config` -> `extract_hoa_data` -> `ocr_extracted_data` -> `store`

## Directory

```md
├── .devcontainer/
    ├── devcontainer.json
    ├── docker-compose.yml
    ├── Dockerfile
├── .vscode/
    ├── launch.json
├── conf/
    ├── dev.env
├── scripts/
    ├── generate_tree.ps1
├── src/
    ├── def_py/
        ├── __init__.py
        ├── str_methods.py
├── tests/
    ├── __init__.py
    ├── main_test.py
├── .flake8
├── .gitignore
├── .pylintrc
├── main.py
├── Makefile
├── pyproject.toml
├── README.md
```

## Initial Setup

Most of this is or will be automated in the `Makefile`. I'm being verbose here.

1. **Create the Repository Folder**
   - Initialize a new directory for your repository.
   - Optionally, run `git init` to initialize a new Git repository.

2. **Generate the Base Files**
   - The `pyproject.toml` file is the most important. Use the VSCode/NVim template to generate this.  It is included below.  Make sure to update `<your_name>`, `<your_email>` and any other parameters like `requires-python` version.
   - Note: Automate this part further as needed, but be aware of potential chicken & egg problems you need to work through.

   ```json
    "pyproject.toml": {
            "prefix": "pyproject",
            "body": [
                "[build-system]",
                "requires = [\"setuptools >= 61.0\"]",
                "build-backend = \"setuptools.build_meta\"",
                "[project]",
                "name = \"$1\"",
                "version = \"0.1.0\"",
                "description = \"$2.\"",
                "requires-python = \">=3.12\"",
                "license = { file = \"LICENSE.txt\" }",
                "keywords = [\"template\",]",
                "authors = [{ name = \"<your_name>\", email = \"<your_email>\" }]",
                "maintainers = [{ name = \"<your_name>\", email = \"<your_email>\" }]",
                "dependencies = [",
                "\t'httpx'",
                "]",
                "",
                "[project.optional-dependencies]",
                "dev = [",
                "\t\"debugpy\",",
                "\t\"pylint\",",
                "\t\"toml\",",
                "\t\"yapf\",",
                "\t\"colorama\",",
                "\t\"isort\",",
                "\t\"black\",",
                "\t\"mypy\",",
                "\t\"pytest\",",
                "\t\"mypy-extensions\",",
                "]",
                "test = [\"pytest < 5.0.0\", \"pytest-cov[all]\"]",
                "cli = [\"click\", \"rich\"]",
                "all = [\"$1[test, dev, cli]\"]",
                "",
                "[project.urls]",
                "homepage = \"https://example.com\"",
                "documentation = \"https://readthedocs.org\"",
                "repository = \"https://github.com/minoad/$1\"",
                "changelog = \"https://github.com/minoad/$1/CHANGELOG.md\"",
                "",
                "[tool.mypy]",
                "warn_unreachable = true",
                "show_error_codes = true",
                "show_column_numbers = true",
                "[tool.pytest.ini_options]",
                "addopts = \"--strict-config --strict-markers\"",
                "",
                "[tool.isort]",
                "profile = \"black\"",
                "",
                "[tool.black]",
                "line-length = 120",
                "target-version = ['py312']",
                "include = '\\.pyi?$'",
                "preview = true",
                "",
                "[tool.pylint.format]",
                "max-line-length = \"120\"",
                "",
                "[tool.pylint.'MESSAGES CONTROL']",
                "max-line-length = 120",
                "",
                "[project.scripts]",
                "$1-cli = \"$1-cli:main_cli\"",
                "#Equivilent to `from spam import main_cli; main_cli()`",
                "#Touch $1/__init__.py",
                "# echo 'def main_cli(): pass' >> $1/__init__.py",
                "",
                "[project.gui-scripts]",
                "$1-gui = \"$1-gui:main_cli\"",
                "# echo 'def main_gui(): pass' >> $1/__init__.py",
                "",
                "# Deploy using pip install -e .[all]",
            ],
        }
   ```

3. **Set Up the Virtual Environment**
   - Ensure that `python` refers to the correct version of the binary.
   - Execute `python -m venv .venv` to create a virtual environment in the `.venv` directory.

4. **Activate the Virtual Environment**
   - **Windows**: Run `.venv\Scripts\Activate.ps1` (or `.venv\Scripts\activate.bat` for Command Prompt).
   - **Mac/Linux**: Run `source .venv/bin/activate`.

5. **Set Up the Source Directory**
   - Create your module structure: `src/<module>/`.
   - Add your variables or functions in `src/<module>/<any_variable_or_function>.py`.
   - Ensure there is a blank `src/<module>/__init__.py` file to make it a package.

6. **Install Your Module in Editable Mode**
   - This uses the details from the `pyproject.toml` file, which includes dependencies.
   - Run `python -m pip install -e .` to install the module in editable mode.

7. **Verify Imports and Functionality**
   - Add the variable or function you defined in your module to `main.py`. For example:

     ```python
     from src.<module> import <any_variable_or_function>
     logger = get_logger()
     ```

## Get to MVP without pytest

Often, you cannot use `pytest` in interviews since it is not part of the standard library. I call the first successful run that meets requirements "MVP". While I prefer the `pytest` option, which we will cover later, I'll first show how to do this without `pytest`.

I created an anagram checker function called `is_anagram()` in `src/def_py/str_methods.py`. Its current contents are below. Right now it only returns `False`. We solve the function only up to two tests passing. No scope creep allowed. When it can tell us that `listen` and `silent` are anagrams and `blue` and `joe` are not anagrams, then we can look at additional items.

```python
def is_anagram(s1: str, s2: str) -> bool:
    return False
```

Under my `tests` directory, I create an `anagram_test.py` file. It contains:

```python
from typing import Any
from def_py import get_logger
from def_py.str_methods import is_anagram

logger = get_logger()

def test_anagram():
    """
    Checks test eval
    """
    test_cases: dict[str, dict[str, Any]] = {
        "simple_anagram": {
            "function": is_anagram,
            "input": {"s1": "Listen", "s2": "Silent"},
            "expected": True,
            "expected_to_fail": False
        },
        "not_anagram": {
            "function": is_anagram,
            "input": {"s1": "blue", "s2": "joe"},
            "expected": False,
            "expected_to_fail": False
        },
    }
    for k, v in test_cases.items():
        try:
            result = v["function"](**v['input'])
            assert result == v["expected"], f"Test {k} failed: expected {v['expected']}, got {result}"
            if v["expected_to_fail"]:
                logger.error(f"Test {k} was expected to fail but passed.")
            else:
                logger.debug(f"Test {k} passed.")
        except Exception as e:
            if v["expected_to_fail"]:
                logger.debug(f"Test {k} failed as expected: {e}")
            else:
                logger.error(f"Test {k} unexpected failure: {e}")

if __name__ == "__main__":
    test_anagram()
```

Running this should produce:

```shell
2024-05-31 16:14:20 ERROR    Test simple_anagram unexpected failure: Test simple_anagram failed: expected True, got False
2024-05-31 16:14:20 ERROR    Test mixed_case unexpected failure: Test mixed_case failed: expected True, got False
```

Now, let's fix that. Since anagrams just need to know that the same number of characters occur with the same frequency, we can just do a quick list comparison.

```python
def is_anagram(s1: str, s2: str) -> bool:
    """
    Checks to see if 2 words are anagrams of each other.

    Args:
        s1 (str): first word to check
        s2 (str): second word to check
    """
    word1: list[str] = sorted([i.lower() for i in s1 if i.isalnum()])
    word2: list[str] = sorted([i.lower() for i in s2 if i.isalnum()])

    anagram = word1 == word2
    logger.info(f"{word1} - {anagram} - {word2}; ")  # pylint: disable=logging-fstring-interpolation
    return anagram
```

Now when we run it, we get the following output:

```shell
2024-05-31 16:23:55 INFO     ['e', 'i', 'l', 'n', 's', 't'] - True - ['e', 'i', 'l', 'n', 's', 't'];
2024-05-31 16:23:55 DEBUG    Test simple_anagram passed.
2024-05-31 16:23:55 INFO     ['e', 'i', 'l', 'n', 's', 't'] - True - ['e', 'i', 'l', 'n', 's', 't'];
2024-05-31 16:23:55 DEBUG    Test mixed_case passed.
```

This is where the fun starts. Come up with any test cases you think are interesting. How about an empty input? What about casing? Is `s` and `S` the same thing in this context? Keep adding test cases. Here is an updated one.

```python
test_cases: Dict[str, Dict[str, Any]] = {
    "simple_anagram": {
        "function": is_anagram,
        "input": {"s1": "Listen", "s2": "Silent"},
        "expected": True,
        "expected_to_fail": False
    },
    "mixed_case": {
        "function": is_anagram,
        "input": {"s1": "Listen", "s2": "silent"},
        "expected": True,
        "expected_to_fail": False
    },
    "non_alphanum": {
        "function": is_anagram,
        "input": {"s1": "Lis;;ten", "s2": "Si'lent"},
        "expected": True,
        "expected_to_fail": False
    },
    "not_anagrams": {
        "function": is_anagram,
        "input": {"s1": "Bob", "s2": "Joe"},
        "expected": False,
        "expected_to_fail": False
    },
    "extra_space": {
        "function": is_anagram,
        "input": {"s1": "Hello", "s2": "Ole Oh"},
        "expected": False,
        "expected_to_fail": False
    },
    "duplicate_characters": {
        "function": is_anagram,
        "input": {"s1": "Lissssten", "s2": "Silent"},
        "expected": False,
        "expected_to_fail": False
    },
    "empty": {
        "function": is_anagram,
        "input": {},
        "expected": False,
        "expected_to_fail": True
    },
}
```

Don't forget to test the sad path. That is the purpose of the `"expected_to_fail"` element in the dictionary. If you want to get an exception or an error, set that to `True`.

## Get to MVP with pytest

If you have access to `pytest`, update your `tests/anagram_test.py` file to this.

```python
# tests/test_your_function.py
import pytest
from src.your_module.your_function import is_anagram

test_cases = {
    "simple_anagram": {
        "function": is_anagram,
        "input": {"s1": "Listen", "s2": "Silent"},
        "expected": True,
        "expected_to_fail": False
    },
    "mixed_case": {
        "function": is_anagram,
        "input": {"s1": "Listen", "s2": "silent"},
        "expected": True,
        "expected_to_fail": False
    },
    "non_alphanum": {
        "function": is_anagram,
        "input": {"s1": "Lis;;ten", "s2": "Si'lent"},
        "expected": True,
        "expected_to_fail": False
    },
    "not_anagrams": {
        "function": is_anagram,
        "input": {"s1": "Bob", "s2": "Joe"},
        "expected": False,
        "expected_to_fail": False
    },
    "extra_space": {
        "function": is_anagram,
        "input": {"s1": "Hello", "s2": "Ole Oh"},
        "expected": False,
        "expected_to_fail": False
    },
    "duplicate_characters": {
        "function": is_anagram,
        "input": {"s1": "Lissssten", "s2": "Silent"},
        "expected": False,
        "expected_to_fail": False
    },
    "empty": {
        "function": is_anagram,
        "input": {},
        "expected": False,
        "expected_to_fail": True
    },
}

@pytest.mark.parametrize("name, case", test_cases.items())
def test_is_anagram(name, case):
    func = case["function"]
    inputs = case["input"]

    # Handle cases where input might be missing or incorrect
    if case["expected_to_fail"]:
        with pytest.raises(Exception):
            func(**inputs)
    else:
        result = func(**inputs)
        assert result == case["expected"], f"Test {name} failed: expected {case['expected']} but got {result}"
```

`pytest /tests/` should now give the following.

```shell
================================================================================================== test session starts ===================================================================================================
platform win32 -- Python 3.12.3, pytest-8.2.1, pluggy-1.5.0
rootdir: rootdir\def_py
configfile: pyproject.toml
plugins: anyio-4.4.0, cov-5.0.0
collected 7 items

tests\anagram_test.py .......                                                                                                                                                                                       [100%]

=================================================================================================== 7 passed in 0.10s ====================================================================================================
```

The beauty here is that we can guarantee that checks pass prior to commits.

Let's execute `python -m pip install pre-commit`.

Create `.pre-commit-config.yaml` at your root with this content.

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.1  # Use the latest stable version
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-added-large-files
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        pass_filenames: false
```

This configuration runs basic checks (trailing whitespace, end-of-file fixer, and large file checks) along with your pytest tests.

Run `pre-commit install`.
Before running pre-commit, I recommend closing all of your files in vscode. You don't want auto save interfering.
Run the below a few times to get all greens. `git add . && git commit -m "testing precommit"`. This will take a minute or so.

When all green, run `git push -u origin main`.

Now let's break a test to see it in action.

In the file `tests/anagram_test.py` swap `test_cases['simple_anagram']['expected']` to false.

Close your files, then run again.

```shell
(.venv) PS C:\Users\Micah\repos\def_py> git commit -m "testing precommit"
Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Check for added large files..............................................Passed
pytest...................................................................Failed
- hook id: pytest
- exit code: 1

============================= test session starts =============================
platform win32 -- Python 3.12.3, pytest-8.2.1, pluggy-1.5.0
rootdir: C:\Users\Micah\repos\def_py
configfile: pyproject.toml
plugins: anyio-4.4.0, cov-5.0.0
collected 7 items

tests\anagram_test.py F......                                            [100%]

================================== FAILURES ===================================
____________________ test_is_anagram[simple_anagram-case0] ____________________

name = 'simple_anagram'
case = {'expected': False, 'expected_to_fail': False, 'function': <function is_anagram at 0x000001837C1425C0>, 'input': {'s1': 'Listen', 's2': 'Silent'}}

    @pytest.mark.parametrize("name, case", test_cases.items())
    def test_is_anagram(name, case):
        func = case["function"]
        inputs = case["input"]

        # Handle cases where input might be missing or incorrect
        if case["expected_to_fail"]:
            with pytest.raises(Exception):
                func(**inputs)
        else:
            result = func(**inputs)
>           assert result == case["expected"], f"Test {name} failed: expected {case['expected']} but got {result}"
E           AssertionError: Test simple_anagram failed: expected False but got True
E           assert True == False

tests\anagram_test.py:68: AssertionError
=========================== short test summary info ===========================
FAILED tests/anagram_test.py::test_is_anagram[simple_anagram-case0] - Asserti...
========================= 1 failed, 6 passed in 0.11s =========================
```

We were prevented. Go back and fix it and you will get a nice green.
