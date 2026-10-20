"""SMTP configuration management."""

import os
from dataclasses import dataclass

from mailcli.exceptions import ConfigurationError


@dataclass(frozen=True, slots=True)
class SMTPConfig:
    """Store the settings required to connect to an SMTP server."""

    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True


def load_smtp_config() -> SMTPConfig:
    """Load and validate SMTP settings from environment variables."""
    host = os.getenv("SMTP_HOST", "").strip()
    port_value = os.getenv("SMTP_PORT", "587").strip()
    username = os.getenv("SMTP_USERNAME", "").strip()
    password = os.getenv("SMTP_PASSWORD", "")
    tls_value = os.getenv("SMTP_USE_TLS", "true").strip().lower()

    if not host:
        raise ConfigurationError("SMTP_HOST is required.")

    try:
        port = int(port_value)
    except ValueError as exc:
        raise ConfigurationError("SMTP_PORT must be an integer.") from exc

    if not 1 <= port <= 65535:
        raise ConfigurationError("SMTP_PORT must be between 1 and 65535.")

    if not username:
        raise ConfigurationError("SMTP_USERNAME is required.")

    if not password:
        raise ConfigurationError("SMTP_PASSWORD is required.")

    if tls_value not in {"true", "false"}:
        raise ConfigurationError("SMTP_USE_TLS must be 'true' or 'false'.")

    return SMTPConfig(
        host=host,
        port=port,
        username=username,
        password=password,
        use_tls=tls_value == "true",
    )
