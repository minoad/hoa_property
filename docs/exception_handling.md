# Systematic Approach to Exception Handling

Follow this systematic approach to decide when and where to catch exceptions:

## 1. Understanding the Context

- **Function Purpose**: Clearly define what `DoThing()` is supposed to do. This helps in identifying what exceptions might naturally arise.
- **Expected Exceptions**: Determine the specific exceptions that could be reasonably expected during the method's execution.

## 2. Ruleset for Exception Handling

### A. Catch Only Known Exceptions

- **Expected Exceptions**: Catch exceptions that are known and anticipated. For example, if the method involves file operations, catch exceptions like `FileNotFoundError` or `IOError`.
- **Unexpected Exceptions**: Avoid catching broad exceptions like `Exception` unless you have a very specific reason.

### B. Use Specific Exception Handling

- **Granular Handling**: Handle specific exceptions where you can take a meaningful action. For instance, catching `ValueError` if the method processes user input that might be invalid.
- **Custom Exceptions**: Define and raise custom exceptions if there are specific error conditions related to the business logic of `GenericThing`.

### C. Logging and Re-Raising

- **Logging**: Log the exceptions to capture sufficient details about the error without stopping the program's flow. This is particularly useful for debugging and auditing.
- **Re-Raising**: Re-raise exceptions if they cannot be handled at the current level but should be managed at a higher level in the application stack.

### D. Clean-up Actions

- **Resource Management**: Use `finally` blocks to ensure that resources are properly released, such as closing files or network connections.

### E. Fail Fast and Clearly

- **Early Exit**: When an error condition is detected that cannot be recovered from within `DoThing()`, fail fast by raising an appropriate exception.
- **Clear Messages**: Provide clear and informative error messages to help diagnose the issue.

## 3. Implementing the Ruleset in `DoThing()`

Here's an example of how you might structure `DoThing()` with these principles:

```python
import logging

class CustomException(Exception):
    pass

class GenericThing:
    def DoThing(self):
        try:
            # Code that might raise exceptions
            self._perform_operation()
        except ValueError as ve:
            logging.error(f"ValueError occurred: {ve}")
            raise CustomException("A specific error occurred in DoThing()") from ve
        except IOError as ioe:
            logging.error(f"IOError occurred: {ioe}")
            raise CustomException("Failed to perform I/O operation") from ioe
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise CustomException("An unexpected error occurred in DoThing()") from e
        finally:
            self._clean_up()

    def _perform_operation(self):
        # Placeholder for the actual operation
        pass

    def _clean_up(self):
        # Placeholder for clean-up actions
        pass
```

## Common Operations and their Exceptions

### 1. File Operations

#### Opening a File

- `FileNotFoundError`: Raised when trying to open a file that does not exist.
- `PermissionError`: Raised when the file cannot be accessed due to permission issues.
- `IsADirectoryError`: Raised when trying to open a directory as a file.
- `IOError`: Generic I/O-related error.

```python
import logging as logger

def open_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Process the file content
            print(content)
    except FileNotFoundError as e:
        logger.error("FileNotFoundError: The file %s does not exist. %s", self.path, e)
        raise e
    except PermissionError as e:
        logger.error("PermissionError: Permission denied to access the file %s: %s", self.path, e)
        raise e
    except IsADirectoryError as e:
        logger.error("IsADirectoryError: %s is a directory, not a file. %s", self.path, e)
        raise e
    except IOError as e:
        logger.error("IOError: An I/O error occurred while accessing the file %s: %s", self.path, e)
        raise e

# Example usage
file_path = 'example.txt'
open_file(file_path)

```

#### Reading/Writing to a File

- `EOFError`: Raised when the end of the file is reached unexpectedly.
- `IOError`: Raised when an I/O operation fails.

### 2. Network Operations

#### Connecting to a Server

- `ConnectionError`: Base class for connection-related errors.
- `TimeoutError`: Raised when a connection times out.
- `socket.error`: Raised for general socket-related errors.

#### Data Transmission

- `socket.timeout`: Raised when a socket operation times out.
- `BrokenPipeError`: Raised when trying to write to a broken pipe or closed socket.

### 3. Database Operations

#### Connecting to a Database

- `OperationalError`: Raised for operational errors (e.g., connection issues).
- `InterfaceError`: Raised for errors related to the database interface.

#### Executing Queries

- `ProgrammingError`: Raised for SQL syntax errors or misuse of the database interface.
- `IntegrityError`: Raised when a database integrity constraint is violated.

### 4. Arithmetic Operations

#### Basic Arithmetic

- `ZeroDivisionError`: Raised when division or modulo by zero is attempted.
- `OverflowError`: Raised when a mathematical operation exceeds the limits for a numeric type.

### 5. Type Conversion

#### Converting Types

- `ValueError`: Raised when a function receives an argument of the correct type but an inappropriate value (e.g., converting a non-numeric string to an integer).
- `TypeError`: Raised when an operation or function is applied to an object of inappropriate type.

### 6. Data Structures

#### Indexing/Slicing

- `IndexError`: Raised when an index is out of range.
- `KeyError`: Raised when a dictionary key is not found.

```python
import logging

def access_list_element(lst, index):
    try:
        element = lst[index]
        print(f"Element at index {index}: {element}")
    except IndexError:
        logging.error(f"IndexError: Index {index} is out of range for the list.")

def access_dict_value(dct, key):
    try:
        value = dct[key]
        print(f"Value for key '{key}': {value}")
    except KeyError:
        logging.error(f"KeyError: The key '{key}' was not found in the dictionary.")

# Example usage
my_list = [1, 2, 3]
my_dict = {'a': 1, 'b': 2, 'c': 3}

# Access list element
index = 5
access_list_element(my_list, index)

# Access dictionary value
key = 'z'
access_dict_value(my_dict, key)
```

#### Attribute Access

- `AttributeError`: Raised when an attribute reference or assignment fails.

### 7. Importing Modules

#### Importing

- `ImportError`: Raised when an import statement fails.
- `ModuleNotFoundError`: Raised when a module could not be found.

### 8. JSON Operations

#### Parsing JSON

- `JSONDecodeError`: Raised when decoding JSON fails.

### 9. General Errors

#### Assertion Errors

- `AssertionError`: Raised when an assert statement fails.

```python
import json
import logging

def parse_json(json_string):
    try:
        data = json.loads(json_string)
        print("Parsed JSON data:", data)
        return data
    except json.JSONDecodeError as e:
        logging.error(f"JSONDecodeError: Failed to decode JSON: {e}")
        return None

# Example usage
json_string_valid = '{"name": "John", "age": 30}'
json_string_invalid = '{"name": "John", "age": 30,}'  # Invalid JSON due to trailing comma

# Parse valid JSON string
parse_json(json_string_valid)

# Parse invalid JSON string
parse_json(json_string_invalid)

```

#### System-Related Errors

- `SystemError`: Raised when the interpreter detects an internal error.
- `OSError`: Raised for operating system-related errors (e.g., file not found, permission denied).

## Summary of Common Exceptions to Consider

- `FileNotFoundError`
- `PermissionError`
- `IsADirectoryError`
- `IOError`
- `EOFError`
- `ConnectionError`
- `TimeoutError`
- `socket.error`
- `socket.timeout`
- `BrokenPipeError`
- `OperationalError`
- `InterfaceError`
- `ProgrammingError`
- `IntegrityError`
- `ZeroDivisionError`
- `OverflowError`
- `ValueError`
- `TypeError`
- `IndexError`
- `KeyError`
- `AttributeError`
- `ImportError`
- `ModuleNotFoundError`
- `JSONDecodeError`
- `AssertionError`
- `SystemError`
- `OSError`
