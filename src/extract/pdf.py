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

    def get_pdf_files(self) -> list[PDFFile]:
        """
        Collect pdf files from a filepath or a directory.
        """
        pdf_files = []
        try:
            p = Path(self.path)
            if p.is_dir():
                pdf_files = [PDFFile(str(file)) for file in p.iterdir() if file.suffix.lower() == ".pdf"]
            elif p.is_file() and p.suffix.lower() == ".pdf":
                pdf_files = [PDFFile(str(p))]
            else:
                logger.error("The path %s is neither a directory nor a PDF file.", self.path)
        except FileNotFoundError as e:
            logger.error("An error occurred while retrieving PDF files: %s", e)
        logger.debug("PDF files found: %s", pdf_files)
        return pdf_files

    def __post_init__(self):

        self.get_pdf_files()
