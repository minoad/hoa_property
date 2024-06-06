"""
Given a pdf or directory containing pdf's:
    - Build objects out of the pdf's.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

# import fitz
import pymupdf

from extract.handler import handle_file_exceptions
from hoa_property import logger


@dataclass()
class PDFFile:
    """
    A class to represent a PDF file.

    This class provides methods to collect PDF metadata and pages from a specified filepath.
    It attempts to open the file and, if successful, collects its metadata and pages.
    If an error occurs during opening, it logs the error and handles the exception.

    Attributes:
        path (str): The path to the PDF file.
        metadata (Optional[Dict[str, Any]]): Metadata of the PDF file.
        pages (Optional[List[Any]]): List of pages in the PDF file.

    Methods:
        get_pdf_file(): Attempts to open the PDF file and collect its metadata and pages.
    """

    path: str
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    pages: Optional[List[Any]] = field(default=None)

    def get_pdf_file_data(self):
        try:
            doc = pymupdf.open(self.path)  # type: pymupdf.Document
        except OSError as e:
            logger.error("An error occurred while opening the PDF file %s: %s", self.path, e)
            handle_file_exceptions(e, self.path)

        if hasattr(doc, "metadata"):
            self.metadata = doc.metadata if doc.metadata else {}
        else:
            self.metadata = {}

        self.pages = list(doc)  # type: ignore

    def __post_init__(self):
        self.get_pdf_file_data()


class PDFDirectoryGeneralException(Exception):
    """
    Exception raised for general errors in the PDFDirectory class.

    This class is a custom exception class that can be used to raise exceptions for
    non-specific errors that occur within the PDFDirectory class.

    Attributes:
       message (str): An optional message that provides more details about the error.
    """


@dataclass()
class PDFDirectory:
    """
    Collect pdf files from a filepath or a directory.
    """

    path: str
    pdf_files: List[PDFFile] = field(default_factory=list)

    def get_pdf_files(self) -> list[PDFFile]:
        """
        Collects PDF files from a specified filepath or directory.

        This method checks if the path is a directory or a single PDF file.
            If it's a directory, it collects all PDF files within the directory.
            If it's a single PDF file, it collects the file.
            If the path is neither a directory nor a PDF file, it logs an error.
            If a FileNotFoundError occurs, it logs the error and returns None.

        Returns:
            list[PDFFile] | None: A list of PDFFile objects if PDF files are found, None otherwise.
        """
        pdf_files: list[PDFFile] = []  # Make mypy stop complaining
        try:
            p = Path(self.path)
            if not p.exists():
                logger.error("The path %s does not exist.", self.path)
                raise FileNotFoundError(f"The path {self.path} does not exist.")
            if p.is_dir():
                pdf_files = [PDFFile(path=str(file)) for file in p.iterdir() if file.suffix.lower() == ".pdf"]
                logger.debug("checking path: %s, found %s", self.path, pdf_files)
                return pdf_files
            if p.is_file() and p.suffix.lower() == ".pdf":
                pdf_files = [PDFFile(path=str(object=p))]
                return pdf_files
            logger.error("The path %s exists, but is neither a directory nor a PDF file.", self.path)
            raise PDFDirectoryGeneralException(
                f"The path {self.path} exists, but is neither a directory nor a PDF file."
            )
        except OSError as e:
            handle_file_exceptions(e, self.path)

    def __post_init__(self):

        self.pdf_files = self.get_pdf_files() or []
