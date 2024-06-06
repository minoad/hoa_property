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
    Represents a single pdf file.
    """

    filepath: str


@dataclass()
class PDFDirectory:
    """
    Collect pdf files from a filepath or a directory.
    """

    path: str

    def get_pdf_files(self) -> list[PDFFile] | None:
        """
        Collect pdf files from a filepath or a directory.
        """
        pdf_files: list[PDFFile] = []  # Make mypy stop complaining
        try:
            p = Path(self.path)
            if p.is_dir():
                pdf_files = [
                    PDFFile(filepath=str(object=file)) for file in p.iterdir() if file.suffix.lower() == ".pdf"
                ]
                return pdf_files
            if p.is_file() and p.suffix.lower() == ".pdf":
                pdf_files = [PDFFile(filepath=str(object=p))]
                return pdf_files
            logger.error("The path %s is neither a directory nor a PDF file.", self.path)
        except FileNotFoundError as e:
            logger.error("An error occurred while retrieving PDF files: %s", e)
        return None

    def __post_init__(self):

        self.get_pdf_files()
