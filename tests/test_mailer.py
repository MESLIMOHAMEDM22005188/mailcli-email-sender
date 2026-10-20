"""Tests for SMTP email delivery."""

from email.message import EmailMessage as MIMEEmailMessage
from unittest.mock import MagicMock, patch

import pytest

from mailcli.config import SMTPConfig
from mailcli.exceptions import EmailSendError
from mailcli.mailer import send_email


@pytest.fixture
def smtp_config():
    return SMTPConfig(
        host="smtp.example.com",
        port=587,
        username="sender@example.com",
        password="test-password",
        use_tls=True,
    )


def test_send_email_uses_starttls_and_sends_message(smtp_config):
    message = MIMEEmailMessage()
    message["From"] = "sender@example.com"
    message["To"] = "recipient@example.com"
    message["Subject"] = "Test"
    message.set_content("Hello")

    with patch("mailcli.mailer.smtplib.SMTP") as smtp_class:
        server = MagicMock()
        smtp_class.return_value.__enter__.return_value = server

        send_email(message, smtp_config)

    smtp_class.assert_called_once_with(
        "smtp.example.com",
        587,
        timeout=30,
    )
    server.starttls.assert_called_once()
    server.login.assert_called_once_with("sender@example.com", "test-password")
    server.send_message.assert_called_once_with(message)


def test_send_email_without_tls_skips_starttls(smtp_config):
    message = MIMEEmailMessage()
    message["From"] = "sender@example.com"
    message["To"] = "recipient@example.com"
    message["Subject"] = "Test"
    message.set_content("Hello")
    config = SMTPConfig(
        host=smtp_config.host,
        port=smtp_config.port,
        username=smtp_config.username,
        password=smtp_config.password,
        use_tls=False,
    )

    with patch("mailcli.mailer.smtplib.SMTP") as smtp_class:
        server = MagicMock()
        smtp_class.return_value.__enter__.return_value = server

        send_email(message, config)

    server.starttls.assert_not_called()
    server.send_message.assert_called_once_with(message)


def test_send_email_wraps_smtp_errors(smtp_config):
    message = MIMEEmailMessage()

    with patch(
        "mailcli.mailer.smtplib.SMTP",
        side_effect=OSError("connection failed"),
    ):
        with pytest.raises(EmailSendError, match="connection failed"):
            send_email(message, smtp_config)
