"""
Given a pdf or directory containing pdf's:
    - Build objects out of the pdf's.
"""

from dataclasses import dataclass
from pathlib import Path

from hoa_property import logger


@dataclass()
class PDFFile:
    """
    A class to represent a directory of PDF files.

    This class provides methods to collect PDF files from a specified filepath or directory.
    It checks if the path is a directory or a single PDF file. If it's a directory, it collects
    all PDF files within the directory. If it's a single PDF file, it collects the file.
    If the path is neither a directory nor a PDF file, it logs an error.
    If a FileNotFoundError occurs, it logs the error and returns None.

    Attributes:
        path (str): The path to the directory or file.

    Methods:
        get_pdf_files(): Collects PDF files from the specified filepath or directory.
    """

    filepath: str


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
            if p.is_dir():
                pdf_files = [PDFFile(filepath=str(file)) for file in p.iterdir() if file.suffix.lower() == ".pdf"]
                logger.debug("checking path: %s, found %s", self.path, pdf_files)
                return pdf_files
            if p.is_file() and p.suffix.lower() == ".pdf":
                pdf_files = [PDFFile(filepath=str(object=p))]
                return pdf_files
            logger.error("The path %s is neither a directory nor a PDF file.", self.path)
        except FileNotFoundError as e:
            logger.error("An error occurred while retrieving PDF files: %s", e)
            raise e

        raise PDFDirectoryGeneralException(f"An error occurred while retrieving PDF files fro {self.path}.")

    def __post_init__(self):

        self.get_pdf_files()
