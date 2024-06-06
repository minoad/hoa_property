from typing import Any

import pytest

from extract.pdf import PDFDirectory
from hoa_property import logger

test_cases: dict[str, dict[str, Any]] = {
    "invalid_path": {
        "function": lambda: PDFDirectory(path="invalid/path").path,
        "expected": None,
        "expected_to_fail": True,
    },
    "multi_pdfs_in_path": {
        "function": lambda: PDFDirectory(path="data/test/plats").path,
        "expected": "data/test/plats",
        "expected_to_fail": False,
    },
    "single_pdfs_in_path": {
        "function": lambda: PDFDirectory(path="data/test/plats/Cap Rock 1 Recorded Plat.pdf").path,
        # "input": {"path": "data/test/plats/Cap Rock 1 Recorded Plat.pdf"},
        "expected": "data/test/plats/Cap Rock 1 Recorded Plat.pdf",
        "expected_to_fail": False,
    },
    "pdf_file_has_metadata_and_pages": {
        "function": lambda: (
            bool(PDFDirectory(path="data/test/plats/Cap Rock 1 Recorded Plat.pdf").pdf_files[0].metadata)
        ),
        "expected": True,  # result.pdf_files[0].metadata
        "expected_to_fail": False,
    },
}


@pytest.mark.parametrize("name, case", test_cases.items())
def test_pdfs(name, case):
    """
    Tests the PDF processing functions with various test cases.

    This function is parameterized with a dictionary of test cases. Each test case is a dictionary
    that includes the function to be tested, the input for the function, the expected result, and
    a flag indicating whether the test case is expected to fail.

    If the test case is expected to fail, the function checks that an exception is raised.
    Otherwise, it checks that the function returns the expected result.

    Args:
        name (str): The name of the test case.
        case (dict): The test case. It should have the following keys:
            - "function": The function to be tested.
            - "input": The input for the function.
            - "expected": The expected result.
            - "expected_to_fail": A flag indicating whether the test case is expected to fail.

    Raises:
        Exception: If the test case is expected to fail and no exception is raised.
        AssertionError: If the function does not return the expected result.
    """
    func = case["function"]
    # inputs = case["input"]

    # Handle cases where input might be missing or incorrect
    if case["expected_to_fail"]:
        with pytest.raises(Exception):
            result = func()
    else:
        # result = func(**inputs)
        result = func()
        logger.debug("%s == %s", result, case["expected"])
        assert result == case["expected"], f"Test {name} failed: expected {case['expected']} but got {result}"

        # Execute custom checks if provided in the test case
        if "custom_check" in case:
            case["custom_check"](result)


if __name__ == "__main__":
    pytest.main()
