from __future__ import annotations

from pathlib import Path

from opml_lib.reader import read_opml
from opml_lib.writer import write_opml


def test_write_basic_opml(tmp_path: Path):
    """Test writing a basic OPML file."""
    output_file = tmp_path / "output.opml"
    data = [
        {"title": "Test Feed", "url": "https://example.com/feed.xml", "link": "https://example.com"}
    ]

    write_opml(data, str(output_file), "Test Title")

    assert output_file.exists()
    content = output_file.read_text()
    assert '<?xml version="1.0" encoding="UTF-8"?>' in content
    assert "<title>Test Title</title>" in content
    assert 'text="Test Feed"' in content
    assert 'xmlUrl="https://example.com/feed.xml"' in content
    assert 'htmlUrl="https://example.com"' in content


def test_write_multiple_feeds(tmp_path: Path):
    """Test writing multiple feeds to OPML."""
    output_file = tmp_path / "multiple.opml"
    data = [
        {"title": "Feed 1", "url": "https://feed1.com/rss", "link": "https://feed1.com"},
        {"title": "Feed 2", "url": "https://feed2.com/rss", "link": "https://feed2.com"},
        {"title": "Feed 3", "url": "https://feed3.com/rss", "link": "https://feed3.com"},
    ]

    write_opml(data, str(output_file))

    content = output_file.read_text()
    assert 'text="Feed 1"' in content
    assert 'text="Feed 2"' in content
    assert 'text="Feed 3"' in content


def test_write_with_special_characters(tmp_path: Path):
    """Test that special XML characters are properly escaped."""
    output_file = tmp_path / "special.opml"
    data = [
        {"title": "Test & Demo", "url": "https://example.com/feed.xml", "link": "https://example.com"}
    ]

    write_opml(data, str(output_file))

    content = output_file.read_text()
    # Jinja2's |e filter should escape the ampersand
    assert "&amp;" in content or "Test &amp; Demo" in content


def test_write_with_none_link(tmp_path: Path):
    """Test writing OPML when link is None."""
    output_file = tmp_path / "none_link.opml"
    data = [
        {"title": "No Link", "url": "https://example.com/feed.xml", "link": None}
    ]

    write_opml(data, str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert 'text="No Link"' in content


def test_write_empty_list(tmp_path: Path):
    """Test writing an empty feed list."""
    output_file = tmp_path / "empty.opml"
    data = []  # type: ignore[var-annotated]

    write_opml(data, str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert "<opml version=" in content
    assert "<body>" in content
    assert "</body>" in content


def test_roundtrip_read_write(tmp_path: Path):
    """Test that data can be read and written back."""
    output_file = tmp_path / "roundtrip.opml"
    original_data = [
        {"title": "Python Podcast", "url": "https://pythonpodcast.com/rss.xml", "link": "https://pythonpodcast.com"},
        {"title": "Tech News", "url": "https://technews.example.com/feed.xml", "link": "https://technews.example.com"},
    ]

    # Write the data
    write_opml(original_data, str(output_file), "Roundtrip Test")

    # Read it back
    read_data = read_opml(str(output_file))

    # Compare (note: read_opml sorts by title)
    assert len(read_data) == len(original_data)
    for entry in original_data:
        # Find matching entry in read_data
        matches = [r for r in read_data if r["url"] == entry["url"]]
        assert len(matches) == 1
        assert matches[0]["link"] == entry["link"]


def test_write_default_title(tmp_path: Path):
    """Test that default title is used when not specified."""
    output_file = tmp_path / "default_title.opml"
    data = [
        {"title": "Test", "url": "https://example.com/feed.xml", "link": "https://example.com"}
    ]

    write_opml(data, str(output_file))

    content = output_file.read_text()
    assert "<title>OPML output</title>" in content


def test_write_custom_title(tmp_path: Path):
    """Test writing with custom title."""
    output_file = tmp_path / "custom_title.opml"
    data = [
        {"title": "Test", "url": "https://example.com/feed.xml", "link": "https://example.com"}
    ]

    write_opml(data, str(output_file), "My Custom Title")

    content = output_file.read_text()
    assert "<title>My Custom Title</title>" in content
