import httpx
import pytest

from devhub.integrations import gitlab_client


@pytest.fixture
def captured(monkeypatch):
    calls = []

    def fake_get(url, **kwargs):
        calls.append({"url": url, **kwargs})
        request = httpx.Request("GET", url, params=kwargs.get("params"))
        return httpx.Response(200, json=[{"iid": 3}], request=request)

    monkeypatch.setenv("CODEHOST_TOKEN_gitlab_example_com", "secret-token")
    monkeypatch.setattr(gitlab_client.httpx, "get", fake_get)
    return calls


def test_fetches_open_merge_requests_over_https(captured):
    merge_requests = gitlab_client.fetch_open_merge_requests(
        "gitlab.example.com", "team/service"
    )

    assert merge_requests == [{"iid": 3}]
    assert captured[0]["url"] == (
        "https://gitlab.example.com/api/v4/projects/team%2Fservice/merge_requests"
    )
    assert captured[0]["params"] == {"state": "opened"}
    assert captured[0]["headers"] == {"Authorization": "Bearer secret-token"}


@pytest.mark.parametrize("host", ["evil.com/path", "host:8080", "", "a b"])
def test_rejects_invalid_host(captured, host):
    with pytest.raises(ValueError, match="Invalid host"):
        gitlab_client.fetch_open_merge_requests(host, "team/service")
    assert captured == []


@pytest.mark.parametrize(
    "repo", ["team", "team/service/extra", "../etc", "team/..", "team/se rvice"]
)
def test_rejects_invalid_repo(captured, repo):
    with pytest.raises(ValueError, match="Invalid repo"):
        gitlab_client.fetch_open_merge_requests("gitlab.example.com", repo)
    assert captured == []
