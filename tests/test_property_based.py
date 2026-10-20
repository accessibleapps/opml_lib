from __future__ import annotations

import tempfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

from hypothesis import given
from hypothesis import strategies as st

from opml_lib.reader import read_opml
from opml_lib.writer import write_opml


# Strategy for generating valid feed entries
# Filter out invalid XML characters and control characters
def is_valid_xml_text(s: str) -> bool:
    """Check if string contains only valid XML characters."""
    if not s.strip():
        return False
    # Filter out control characters except tab, newline, carriage return
    for char in s:
        code = ord(char)
        if code < 0x20 and code not in (0x09, 0x0A, 0x0D):
            return False
        # Also exclude surrogates and other problematic ranges
        if 0xD800 <= code <= 0xDFFF or code >= 0x110000:
            return False
    return True


feed_entry = st.fixed_dictionaries(
    {
        "title": st.text(
            alphabet=st.characters(min_codepoint=0x20, max_codepoint=0xD7FF, blacklist_categories=("Cs",)),
            min_size=1,
            max_size=100,
        ).filter(is_valid_xml_text),
        "url": st.from_regex(r"https?://[a-z0-9.-]+\.[a-z]{2,}/[a-z0-9/._-]*", fullmatch=True),
        "link": st.one_of(st.none(), st.from_regex(r"https?://[a-z0-9.-]+\.[a-z]{2,}", fullmatch=True)),
    }
)


@given(st.lists(feed_entry, min_size=0, max_size=50))
def test_write_opml_always_creates_valid_xml(feed_list: list) -> None:  # type: ignore[misc]
    """Test that write_opml always creates valid XML structure."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".opml") as f:
        output_file = f.name

    try:
        write_opml(feed_list, output_file, "Property Test")

        # Check file exists and has content
        path = Path(output_file)
        assert path.exists()
        content = path.read_text(encoding="utf-8")

        # Basic XML structure checks
        assert '<?xml version="1.0" encoding="UTF-8"?>' in content
        assert "<opml version=" in content
        assert "<head>" in content
        assert "</head>" in content
        assert "<body>" in content
        assert "</body>" in content
        assert "</opml>" in content

    finally:
        Path(output_file).unlink()


@given(st.lists(feed_entry, min_size=1, max_size=20))
def test_roundtrip_preserves_urls(feed_list: list) -> None:  # type: ignore[misc]
    """Test that URLs are preserved in read/write roundtrip."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".opml") as f:
        output_file = f.name

    try:
        # Write the data
        write_opml(feed_list, output_file, "Roundtrip Test")

        # Read it back
        result = read_opml(output_file)

        # All original URLs should be present in result
        original_urls = {entry["url"] for entry in feed_list}
        result_urls = {entry["url"] for entry in result}
        assert original_urls == result_urls

    finally:
        Path(output_file).unlink()


@given(st.lists(feed_entry, min_size=1, max_size=20))
def test_roundtrip_preserves_urls_and_links(feed_list: list) -> None:  # type: ignore[misc]
    """Test that feed URLs and nullable HTML links survive a read/write roundtrip."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".opml") as f:
        output_file = f.name

    try:
        write_opml(feed_list, output_file, "Roundtrip Test")
        result = read_opml(output_file)

        original_pairs = Counter((entry["url"], entry["link"]) for entry in feed_list)
        result_pairs = Counter((entry["url"], entry["link"]) for entry in result)
        assert original_pairs == result_pairs

    finally:
        Path(output_file).unlink()


@given(st.lists(feed_entry, min_size=0, max_size=20))
def test_write_opml_returns_none(feed_list: list) -> None:  # type: ignore[misc]
    """Test that write_opml returns None (no exceptions)."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".opml") as f:
        output_file = f.name

    try:
        result = write_opml(feed_list, output_file)
        assert result is None
    finally:
        Path(output_file).unlink()


@given(
    st.text(
        alphabet=st.characters(min_codepoint=0x20, max_codepoint=0xD7FF, blacklist_categories=("Cs",)),
        min_size=1,
        max_size=200,
    ).filter(is_valid_xml_text),
    st.lists(feed_entry, min_size=0, max_size=10),
)
def test_custom_title_appears_in_output(title: str, feed_list: list) -> None:  # type: ignore[misc]
    """Test that custom titles are properly included in OPML."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".opml") as f:
        output_file = f.name

    try:
        write_opml(feed_list, output_file, title)
        content = Path(output_file).read_text(encoding="utf-8")

        # Title should appear in the head section
        assert "<head>" in content
        root = ElementTree.fromstring(content)
        assert root.findtext("./head/title") == title

    finally:
        Path(output_file).unlink()


@given(
    st.text(
        alphabet=st.characters(min_codepoint=0x20, max_codepoint=0xD7FF, blacklist_categories=("Cs",)),
        min_size=1,
        max_size=100,
    ).filter(is_valid_xml_text),
    st.lists(feed_entry, min_size=0, max_size=10),
)
def test_custom_title_keeps_output_parseable(title: str, feed_list: list) -> None:  # type: ignore[misc]
    """Test that arbitrary valid OPML titles are escaped as parseable XML text."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".opml") as f:
        output_file = f.name

    try:
        write_opml(feed_list, output_file, title)
        content = Path(output_file).read_text(encoding="utf-8")

        root = ElementTree.fromstring(content)
        parsed_title = root.findtext("./head/title")
        assert parsed_title == title

    finally:
        Path(output_file).unlink()


@given(st.lists(feed_entry, min_size=1, max_size=50))
def test_read_preserves_entry_count(feed_list: list) -> None:  # type: ignore[misc]
    """Test that reading OPML preserves entry count."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".opml") as f:
        output_file = f.name

    try:
        write_opml(feed_list, output_file)
        result = read_opml(output_file)

        # Should have same number of entries
        assert len(result) == len(feed_list)

    finally:
        Path(output_file).unlink()


@given(st.lists(feed_entry, min_size=2, max_size=20))
def test_read_returns_sorted_list(feed_list: list) -> None:  # type: ignore[misc]
    """Test that read_opml returns entries sorted by title."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".opml") as f:
        output_file = f.name

    try:
        write_opml(feed_list, output_file)
        result = read_opml(output_file)

        # Check that titles are sorted
        titles = [entry["title"] for entry in result]
        assert titles == sorted(titles)

    finally:
        Path(output_file).unlink()
