import pytest

from devhub.api.config import load_host_config


def test_reads_token_from_environment(monkeypatch):
    monkeypatch.setenv("CODEHOST_TOKEN_git_example_com", "secret-token")
    assert load_host_config("git.example.com").token == "secret-token"


def test_missing_token_raises(monkeypatch):
    monkeypatch.delenv("CODEHOST_TOKEN_git_example_com", raising=False)
    with pytest.raises(LookupError):
        load_host_config("git.example.com")


def test_token_is_hidden_from_repr(monkeypatch):
    monkeypatch.setenv("CODEHOST_TOKEN_git_example_com", "secret-token")
    assert "secret-token" not in repr(load_host_config("git.example.com"))
