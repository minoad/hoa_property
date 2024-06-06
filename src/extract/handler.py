from typing import NoReturn

from hoa_property import logger


def handle_file_exceptions(e: Exception, path: str = "") -> NoReturn:
    """
    Handle exceptions for file operations.

    Args:
        e (Exception): The exception to handle.
    """
    if isinstance(e, FileNotFoundError):
        logger.error("FileNotFoundError: The file %s does not exist. %s", path, e)
    elif isinstance(e, PermissionError):
        logger.error("PermissionError: Permission denied to access the file %s: %s", path, e)
    elif isinstance(e, IsADirectoryError):
        logger.error("IsADirectoryError: %s is a directory, not a file. %s", path, e)
    elif isinstance(e, IOError):
        logger.error("IOError: An I/O error occurred while accessing the file %s: %s", path, e)
    else:
        logger.error("An unexpected error occurred: %s", e)
    raise e
