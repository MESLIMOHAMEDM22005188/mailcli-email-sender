"""SMTP email delivery for MailCLI."""

import smtplib
import ssl
from email.message import EmailMessage as MIMEEmailMessage

from mailcli.config import SMTPConfig
from mailcli.exceptions import EmailSendError


def send_email(
    message: MIMEEmailMessage,
    config: SMTPConfig,
) -> None:
    """Send an email through the configured SMTP server."""
    try:
        context = ssl.create_default_context()

        with smtplib.SMTP(config.host, config.port, timeout=30) as server:
            server.ehlo()

            if config.use_tls:
                server.starttls(context=context)
                server.ehlo()

            server.login(config.username, config.password)
            server.send_message(message)

    except (smtplib.SMTPException, OSError) as exc:
        raise EmailSendError(f"Failed to send email: {exc}") from exc
