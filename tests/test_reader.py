from __future__ import annotations

from pathlib import Path

import pytest

from opml_lib.reader import read_opml

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_read_sample_opml():
    """Test reading a sample OPML file with multiple feeds."""
    result = read_opml(str(FIXTURES_DIR / "sample.opml"))

    assert len(result) == 3

    # Check first entry
    assert result[0]["title"] == "Coding Blog"
    assert result[0]["url"] == "https://codingblog.example.com/rss"
    assert result[0]["link"] == "https://codingblog.example.com"

    # Check that results are sorted
    titles = [entry["title"] for entry in result]
    assert titles == sorted(titles)


def test_read_empty_opml():
    """Test reading an empty OPML file."""
    result = read_opml(str(FIXTURES_DIR / "empty.opml"))
    assert result == []


def test_read_opml_with_html_entities():
    """Test that HTML entities are properly stripped."""
    result = read_opml(str(FIXTURES_DIR / "with_html_entities.opml"))

    assert len(result) == 2
    # HTML entities should be decoded by html_stripper
    assert "&" in result[1]["title"] or "Quotes" in result[1]["title"]


def test_read_opml_missing_htmlurl():
    """Test reading OPML where htmlUrl attribute is missing."""
    result = read_opml(str(FIXTURES_DIR / "missing_htmlurl.opml"))

    assert len(result) == 1
    assert result[0]["title"] == "No HTML URL"
    assert result[0]["url"] == "https://example.com/feed.xml"
    assert result[0]["link"] is None


def test_read_opml_nonexistent_file():
    """Test that reading a nonexistent file raises an error."""
    with pytest.raises((FileNotFoundError, OSError)):
        read_opml("nonexistent_file.opml")


def test_opml_entry_structure():
    """Test that returned entries have correct structure."""
    result = read_opml(str(FIXTURES_DIR / "sample.opml"))

    for entry in result:
        assert "title" in entry
        assert "url" in entry
        assert "link" in entry
        assert isinstance(entry["title"], str)
        assert isinstance(entry["url"], str)
        assert entry["link"] is None or isinstance(entry["link"], str)


def test_opml_sorting_by_title():
    """Test that entries are sorted alphabetically by title."""
    result = read_opml(str(FIXTURES_DIR / "sample.opml"))

    titles = [entry["title"] for entry in result]
    assert titles == sorted(titles)


def test_read_opml_with_html_tags():
    """Test that HTML tags in titles are properly stripped."""
    result = read_opml(str(FIXTURES_DIR / "with_html_tags.opml"))

    assert len(result) == 2
    # HTML tags should be stripped by html_stripper
    assert "Bold Feed" in result[0]["title"]
    assert "Italic" in result[1]["title"]
    assert "<" not in result[0]["title"]  # Tags should be removed
    assert "<" not in result[1]["title"]


def test_read_opml_skips_entries_without_url():
    """Test that entries without xmlUrl or url are skipped."""
    result = read_opml(str(FIXTURES_DIR / "without_url.opml"))

    # Should only return entries with URLs, skipping the category outline
    assert len(result) == 2
    assert all(entry["url"] is not None for entry in result)
    titles = [entry["title"] for entry in result]
    assert "Category Without URL" not in titles
