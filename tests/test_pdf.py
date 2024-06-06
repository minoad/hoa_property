from typing import Any

import pytest

from extract.pdf import PDFDirectory
from hoa_property import logger

TEST_PDF_PATH = "data/test/plats"


pdf_files = PDFDirectory(TEST_PDF_PATH)


test_cases: dict[str, dict[str, Any]] = {
    "invalid_path": {
        "function": PDFDirectory,
        "input": {"path": "invalid/path"},
        "expected": None,
        "expected_to_fail": True,
    },
    "multi_pdfs_in_path": {
        "function": PDFDirectory,
        "input": {"path": "data/test/plats"},
        "expected": PDFDirectory(path="data/test/plats"),
        "expected_to_fail": False,
    },
    "single_pdfs_in_path": {
        "function": PDFDirectory,
        "input": {"path": "data/test/plats/Cap Rock 1 Recorded Plat.pdf"},
        "expected": PDFDirectory(path="data/test/plats/Cap Rock 1 Recorded Plat.pdf"),
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
    inputs = case["input"]

    # Handle cases where input might be missing or incorrect
    if case["expected_to_fail"]:
        with pytest.raises(Exception):
            result = func(**inputs)
    else:
        result = func(**inputs)
        assert result == case["expected"], f"Test {name} failed: expected {case['expected']} but got {result}"


logger.debug(pdf_files)

if __name__ == "__main__":
    pytest.main()
