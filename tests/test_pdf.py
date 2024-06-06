from typing import Any

import pymupdf
import pytest

from extract.pdf import PDFDirectory, PDFFile
from hoa_property import logger

test_cases: dict[str, dict[str, Any]] = {
    "invalid_path": {
        "function": lambda: PDFDirectory(path="invalid/path").path,
        "expected": None,
        "expected_exception": FileNotFoundError,
    },
    "multi_pdfs_in_path": {
        "function": lambda: PDFDirectory(path="data/test/plats").path,
        "expected": "data/test/plats",
    },
    "single_pdfs_in_path": {
        "function": lambda: PDFDirectory(path="data/test/plats/Cap Rock 1 Recorded Plat.pdf").path,
        "expected": "data/test/plats/Cap Rock 1 Recorded Plat.pdf",
    },
    "pdf_file_has_metadata_and_pages": {
        "function": lambda: (
            bool(PDFDirectory(path="data/test/plats/Cap Rock 1 Recorded Plat.pdf").pdf_files[0].metadata)
        ),
        "expected": True,
    },
    "pdf_file_does_not_exist": {
        "function": lambda: PDFFile(path="invalid/path"),
        "expected_exception": pymupdf.FileNotFoundError,
        "expected": True,
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

    # Handle cases where input might be missing or incorrect
    if case.get("expected_exception", None):
        with pytest.raises(case["expected_exception"]):
            result = func()
    else:
        result = func()
        logger.debug("%s == %s", result, case["expected"])
        assert result == case["expected"], f"Test {name} failed: expected {case['expected']} but got {result}"


if __name__ == "__main__":
    pytest.main()
