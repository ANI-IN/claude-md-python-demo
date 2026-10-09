import httpx
import pytest

from devhub.integrations import github_client


@pytest.fixture
def captured(monkeypatch):
    calls = []

    def fake_get(url, **kwargs):
        calls.append({"url": url, **kwargs})
        request = httpx.Request("GET", url, params=kwargs.get("params"))
        return httpx.Response(200, json=[{"number": 7}], request=request)

    monkeypatch.setenv("CODEHOST_TOKEN_git_example_com", "secret-token")
    monkeypatch.setattr(github_client.httpx, "get", fake_get)
    return calls


def test_fetches_open_pull_requests_over_https(captured):
    pulls = github_client.fetch_open_pull_requests("git.example.com", "team/service")

    assert pulls == [{"number": 7}]
    assert (
        captured[0]["url"] == "https://git.example.com/api/v3/repos/team/service/pulls"
    )
    assert captured[0]["params"] == {"state": "open"}
    assert captured[0]["headers"] == {"Authorization": "Bearer secret-token"}


@pytest.mark.parametrize("host", ["evil.com/path", "host:8080", "", "a b"])
def test_rejects_invalid_host(captured, host):
    with pytest.raises(ValueError, match="Invalid host"):
        github_client.fetch_open_pull_requests(host, "team/service")
    assert captured == []


@pytest.mark.parametrize(
    "repo", ["team", "team/service/extra", "../etc", "team/..", "team/se rvice"]
)
def test_rejects_invalid_repo(captured, repo):
    with pytest.raises(ValueError, match="Invalid repo"):
        github_client.fetch_open_pull_requests("git.example.com", repo)
    assert captured == []
