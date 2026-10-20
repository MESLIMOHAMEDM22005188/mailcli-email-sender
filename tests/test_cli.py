"""Tests for the MailCLI command-line interface."""

from unittest.mock import patch

from mailcli.cli import create_parser, main


def test_parser_accepts_required_arguments():
    args = create_parser().parse_args(
        [
            "--from", "sender@example.com",
            "--to", "one@example.com", "two@example.com",
            "--subject", "Test",
            "--body", "Hello",
            "--dry-run",
        ]
    )

    assert args.sender == "sender@example.com"
    assert args.recipients == ["one@example.com", "two@example.com"]
    assert args.dry_run is True


def test_main_dry_run_does_not_send(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        [
            "mailcli",
            "--from", "sender@example.com",
            "--to", "recipient@example.com",
            "--subject", "Test",
            "--body", "Hello",
            "--dry-run",
        ],
    )

    with patch("mailcli.cli.send_email") as send_mock:
        assert main() == 0

    send_mock.assert_not_called()
    assert "Dry run successful" in capsys.readouterr().out


def test_main_sends_email_when_not_dry_run(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        [
            "mailcli",
            "--from", "sender@example.com",
            "--to", "recipient@example.com",
            "--subject", "Test",
            "--body", "Hello",
        ],
    )

    with patch("mailcli.cli.load_smtp_config") as config_mock, patch(
        "mailcli.cli.send_email"
    ) as send_mock:
        assert main() == 0

    config_mock.assert_called_once()
    send_mock.assert_called_once()
    assert "Email sent successfully" in capsys.readouterr().out
