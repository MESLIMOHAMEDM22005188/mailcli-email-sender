"""Tests for MIME email message construction."""

from email.message import EmailMessage as MIMEEmailMessage

import pytest

from mailcli.exceptions import MessageError
from mailcli.message_builder import build_message
from mailcli.models import EmailMessage


def make_email(**overrides):
    values = {
        "sender": "sender@example.com",
        "recipients": ["one@example.com", "two@example.com"],
        "subject": "Test subject",
        "body": "Hello from MailCLI",
    }
    values.update(overrides)
    return EmailMessage(**values)


def test_build_plain_text_message():
    message = build_message(make_email())

    assert isinstance(message, MIMEEmailMessage)
    assert message["From"] == "sender@example.com"
    assert message["To"] == "one@example.com, two@example.com"
    assert message["Subject"] == "Test subject"
    assert message.get_content_type() == "text/plain"
    assert "Hello from MailCLI" in message.get_content()


def test_build_html_message():
    message = build_message(make_email(html=True, body="<h1>Hello</h1>"))

    assert message.get_content_type() == "text/html"
    assert "<h1>Hello</h1>" in message.get_content()


@pytest.mark.parametrize(
    ("overrides", "error"),
    [
        ({"sender": " "}, "sender address"),
        ({"recipients": []}, "recipient"),
        ({"recipients": [""]}, "Recipient"),
        ({"subject": " "}, "subject"),
    ],
)
def test_build_message_rejects_invalid_fields(overrides, error):
    with pytest.raises(MessageError, match=error):
        build_message(make_email(**overrides))


def test_build_message_adds_attachment(tmp_path):
    attachment = tmp_path / "note.txt"
    attachment.write_text("attachment content", encoding="utf-8")

    message = build_message(make_email(attachments=[attachment]))
    parts = list(message.iter_attachments())

    assert len(parts) == 1
    assert parts[0].get_filename() == "note.txt"
    assert parts[0].get_content() == b"attachment content"


def test_build_message_rejects_missing_attachment(tmp_path):
    missing = tmp_path / "missing.txt"

    with pytest.raises(MessageError, match="Attachment does not exist"):
        build_message(make_email(attachments=[missing]))
