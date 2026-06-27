"""
pipeline_exceptions.py

Custom exception classes for the Healthcare Analytics Agent
Master Pipeline.

Using custom exceptions makes it easier to identify which
pipeline stage failed and display meaningful error messages
to both users and developers.
"""


class PipelineException(Exception):
    """
    Base exception for all pipeline-related errors.
    """

    def __init__(self, stage: str, message: str):
        self.stage = stage
        self.message = message
        super().__init__(f"[{stage}] {message}")


# -------------------------------------------------------------------
# Validation
# -------------------------------------------------------------------

class ValidationException(PipelineException):
    """
    Raised when dataset validation fails.
    """

    def __init__(self, message: str):
        super().__init__("Validation", message)


# -------------------------------------------------------------------
# Preprocessing
# -------------------------------------------------------------------

class PreprocessingException(PipelineException):
    """
    Raised when preprocessing fails.
    """

    def __init__(self, message: str):
        super().__init__("Preprocessing", message)


# -------------------------------------------------------------------
# Underwriting
# -------------------------------------------------------------------

class UnderwritingException(PipelineException):
    """
    Raised when the underwriting pipeline fails.
    """

    def __init__(self, message: str):
        super().__init__("Underwriting", message)


# -------------------------------------------------------------------
# Pricing
# -------------------------------------------------------------------

class PricingException(PipelineException):
    """
    Raised when the pricing pipeline fails.
    """

    def __init__(self, message: str):
        super().__init__("Pricing", message)


# -------------------------------------------------------------------
# Lapse
# -------------------------------------------------------------------

class LapseException(PipelineException):
    """
    Raised when the lapse prediction pipeline fails.
    """

    def __init__(self, message: str):
        super().__init__("Lapse", message)


# -------------------------------------------------------------------
# Portfolio
# -------------------------------------------------------------------

class PortfolioException(PipelineException):
    """
    Raised when portfolio analytics fails.
    """

    def __init__(self, message: str):
        super().__init__("Portfolio", message)


# -------------------------------------------------------------------
# Dashboard
# -------------------------------------------------------------------

class DashboardException(PipelineException):
    """
    Raised when dashboard preparation fails.
    """

    def __init__(self, message: str):
        super().__init__("Dashboard", message)


# -------------------------------------------------------------------
# AI Copilot
# -------------------------------------------------------------------

class CopilotException(PipelineException):
    """
    Raised when the AI Copilot encounters an error.
    """

    def __init__(self, message: str):
        super().__init__("AI Copilot", message)


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

class ConfigurationException(PipelineException):
    """
    Raised when project configuration is invalid.
    """

    def __init__(self, message: str):
        super().__init__("Configuration", message)


# -------------------------------------------------------------------
# File System
# -------------------------------------------------------------------

class FileSystemException(PipelineException):
    """
    Raised when required files or directories are missing.
    """

    def __init__(self, message: str):
        super().__init__("File System", message)