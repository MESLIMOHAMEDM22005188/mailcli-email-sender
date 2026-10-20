"""Command-line interface for MailCLI."""

import argparse
import logging

from mailcli import __version__
from mailcli.config import load_smtp_config
from mailcli.exceptions import MailCLIError
from mailcli.mailer import send_email
from mailcli.message_builder import build_message
from mailcli.models import EmailMessage


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="mailcli",
        description="Send emails through an SMTP server.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--from",
        dest="sender",
        required=True,
        help="Sender email address.",
    )
    parser.add_argument(
        "--to",
        dest="recipients",
        nargs="+",
        required=True,
        help="One or more recipient email addresses.",
    )
    parser.add_argument("--subject", required=True, help="Email subject.")
    parser.add_argument("--body", required=True, help="Email body.")
    parser.add_argument(
        "--html",
        action="store_true",
        help="Interpret the body as HTML.",
    )
    parser.add_argument(
        "--attachment",
        action="append",
        default=[],
        help="File to attach. Can be specified multiple times.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build the email without sending it.",
    )
    return parser


def main() -> int:
    """Run the command-line interface."""
    parser = create_parser()
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        email = EmailMessage(
            sender=args.sender,
            recipients=args.recipients,
            subject=args.subject,
            body=args.body,
            html=args.html,
            attachments=args.attachment,
        )
        message = build_message(email)

        if args.dry_run:
            print("Dry run successful. Email was built but not sent.")
            print(f"From: {args.sender}")
            print(f"To: {', '.join(args.recipients)}")
            print(f"Subject: {args.subject}")
            return 0

        config = load_smtp_config()
        send_email(message, config)
        print("Email sent successfully.")
        return 0

    except MailCLIError as exc:
        logging.error("%s", exc)
        return 1
