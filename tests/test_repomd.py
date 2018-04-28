from unittest import mock

import pytest
import lxml

import repomd


@pytest.fixture
def repodata():
    path = 'tests/fixtures/repodata'
    with open(f'{path}/repomd.xml', 'rb') as f:
        raw_index = f.read()
    with open(f'{path}/primary.xml.gz', 'rb') as f:
        raw_primary = f.read()
    return (raw_index, raw_primary)


@mock.patch('repomd.urlopen')
def test_repo_init(mock_urlopen, repodata):
    mock_urlopen.return_value.__enter__.return_value.read.side_effect = repodata
    repo = repomd.Repo('https://example.com')
    assert repo.baseurl == 'https://example.com'
    assert repr(repo) == '<Repo: "https://example.com">'
    assert str(repo) == 'https://example.com'
    assert isinstance(repo._metadata, lxml.etree._Element)


def test_repo_init_lazy():
    repo = repomd.Repo('https://example.com', lazy=True)
    assert repo.baseurl == 'https://example.com'
    assert repo._metadata is None
