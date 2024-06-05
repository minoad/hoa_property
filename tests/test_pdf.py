from typing import Any

import pytest

from extract.pdf import PDFDirectory
from hoa_property import logger

TEST_PDF_PATH = "data/test/plats"


pdf_files = PDFDirectory(TEST_PDF_PATH)


test_cases: dict[str, dict[str, Any]] = {
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
    func = case["function"]
    inputs = case["input"]
    result = func(**inputs)

    # Handle cases where input might be missing or incorrect
    if case["expected_to_fail"]:
        with pytest.raises(Exception):
            func(**inputs)
    else:
        result = func(**inputs)
        assert result == case["expected"], f"Test {name} failed: expected {case['expected']} but got {result}"


logger.debug(pdf_files)

if __name__ == "__main__":
    pytest.main()
