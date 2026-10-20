"""Data models used by MailCLI."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class EmailMessage:
    """Represent an email before it is built or sent."""

    sender: str
    recipients: list[str]
    subject: str
    body: str
    html: bool = False
    attachments: list[Path] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Normalize recipient and attachment collections."""
        self.recipients = list(self.recipients)
        self.attachments = [Path(path) for path in self.attachments]
