"""Custom exceptions used by MailCLI."""


class MailCLIError(Exception):
    """Base exception for errors raised by MailCLI."""


class ConfigurationError(MailCLIError):
    """Raised when the SMTP configuration is invalid or incomplete."""


class MessageError(MailCLIError):
    """Raised when an email message is invalid."""


class EmailSendError(MailCLIError):
    """Raised when an email cannot be sent."""
