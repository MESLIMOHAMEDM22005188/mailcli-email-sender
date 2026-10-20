"""Tests for SMTP configuration loading."""

import pytest

from mailcli.config import SMTPConfig, load_smtp_config
from mailcli.exceptions import ConfigurationError


def set_valid_environment(monkeypatch):
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USERNAME", "user@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "test-password")
    monkeypatch.setenv("SMTP_USE_TLS", "true")


def test_load_smtp_config_with_defaults(monkeypatch):
    set_valid_environment(monkeypatch)
    monkeypatch.delenv("SMTP_PORT", raising=False)
    monkeypatch.delenv("SMTP_USE_TLS", raising=False)

    assert load_smtp_config() == SMTPConfig(
        host="smtp.example.com",
        port=587,
        username="user@example.com",
        password="test-password",
        use_tls=True,
    )


def test_load_smtp_config_without_host(monkeypatch):
    set_valid_environment(monkeypatch)
    monkeypatch.setenv("SMTP_HOST", "  ")

    with pytest.raises(ConfigurationError, match="SMTP_HOST is required"):
        load_smtp_config()


@pytest.mark.parametrize("port", ["abc", "0", "65536"])
def test_load_smtp_config_rejects_invalid_port(monkeypatch, port):
    set_valid_environment(monkeypatch)
    monkeypatch.setenv("SMTP_PORT", port)

    with pytest.raises(ConfigurationError):
        load_smtp_config()


def test_load_smtp_config_rejects_missing_credentials(monkeypatch):
    set_valid_environment(monkeypatch)
    monkeypatch.setenv("SMTP_USERNAME", "")

    with pytest.raises(ConfigurationError, match="SMTP_USERNAME is required"):
        load_smtp_config()


def test_load_smtp_config_rejects_invalid_tls_value(monkeypatch):
    set_valid_environment(monkeypatch)
    monkeypatch.setenv("SMTP_USE_TLS", "sometimes")

    with pytest.raises(ConfigurationError, match="SMTP_USE_TLS"):
        load_smtp_config()


def test_load_smtp_config_supports_disabled_tls(monkeypatch):
    set_valid_environment(monkeypatch)
    monkeypatch.setenv("SMTP_USE_TLS", "false")

    assert load_smtp_config().use_tls is False
