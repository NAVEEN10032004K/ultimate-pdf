"""
Custom exceptions used throughout Ultimate PDF.
"""


class UltimatePDFError(Exception):
    """
    Base exception for all Ultimate PDF errors.
    """

    pass


class PDFNotFoundError(UltimatePDFError):
    """
    Raised when a PDF file cannot be found.
    """

    pass


class InvalidPDFError(UltimatePDFError):
    """
    Raised when the file is not a valid PDF.
    """

    pass


class EmptyInputError(UltimatePDFError):
    """
    Raised when no input files are provided.
    """

    pass


class OutputFileError(UltimatePDFError):
    """
    Raised when the output file cannot be created.
    """

    pass


class PDFPasswordError(UltimatePDFError):
    """
    Raised when a password-protected PDF cannot be opened.
    """

    pass


class PDFOperationError(UltimatePDFError):
    """
    Raised when a PDF operation fails.
    """

    pass


class PageRangeError(UltimatePDFError):
    """
    Raised when an invalid page range is supplied.
    """

    pass
