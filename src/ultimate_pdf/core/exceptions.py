"""
Custom exceptions used throughout Ultimate PDF.
"""


class UltimatePDFError(Exception):
    """Base exception for all Ultimate PDF errors."""


class PDFNotFoundError(UltimatePDFError):
    """Raised when a PDF file cannot be found."""


class InvalidPDFError(UltimatePDFError):
    """Raised when the file is not a valid PDF."""


class EmptyInputError(UltimatePDFError):
    """Raised when no input files are provided."""


class OutputFileError(UltimatePDFError):
    """Raised when the output file cannot be created."""


class PDFPasswordError(UltimatePDFError):
    """Raised when a password-protected PDF cannot be opened."""


class PDFOperationError(UltimatePDFError):
    """Raised when a PDF operation fails."""


class PageRangeError(UltimatePDFError):
    """Raised when an invalid page range is supplied."""
