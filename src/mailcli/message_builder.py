"""Build MIME email messages for MailCLI."""

from email.message import EmailMessage as MIMEEmailMessage
from pathlib import Path

from mailcli.exceptions import MessageError
from mailcli.models import EmailMessage


def build_message(email: EmailMessage) -> MIMEEmailMessage:
    """Convert an EmailMessage model into a MIME email message."""
    if not email.sender.strip():
        raise MessageError("The sender address is required.")

    if not email.recipients:
        raise MessageError("At least one recipient is required.")

    if any(not recipient.strip() for recipient in email.recipients):
        raise MessageError("Recipient addresses cannot be empty.")

    if not email.subject.strip():
        raise MessageError("The email subject is required.")

    message = MIMEEmailMessage()
    message["From"] = email.sender
    message["To"] = ", ".join(email.recipients)
    message["Subject"] = email.subject

    message.set_content(
        email.body,
        subtype="html" if email.html else "plain",
        charset="utf-8",
    )

    for attachment in email.attachments:
        path = Path(attachment)

        if not path.is_file():
            raise MessageError(
                f"Attachment does not exist or is not a file: {path}"
            )

        try:
            data = path.read_bytes()
        except OSError as exc:
            raise MessageError(f"Cannot read attachment: {path}") from exc

        message.add_attachment(
            data,
            maintype="application",
            subtype="octet-stream",
            filename=path.name,
        )

    return message
